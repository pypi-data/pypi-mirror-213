# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime, time
import json

from typing import Type

from django.conf import settings
from django.db import models

from lino.mixins import Modified
from lino.modlib.users.mixins import UserAuthored
from lino_xl.lib.cal.models import BaseSubscription
from lino.api import rt, dd, _

from .utils import get_resource, map_calendar_into_dbModel, map_event_into_dbModel, insert_calendar, insert_event
from .choicelists import AccessRoles, google_status


class CalendarSubscription(BaseSubscription, Modified):
    primary = dd.BooleanField(default=False)
    access_role = AccessRoles.field(default='owner')
    sync_token = dd.CharField(max_length=200, blank=True)
    """Used to retrive only the changed entries from the remote server."""
    page_token = dd.BooleanField(default=False)


dd.inject_field("users.User", "calendar_sync_token", dd.CharField(max_length=200, blank=True))


class DeletedEntry(dd.Model):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedEntry")

    calendar = dd.BooleanField(default=False)
    user = dd.ForeignKey('users.User', null=False, blank=False)
    event_id = dd.CharField(max_length=200, blank=True)
    calendar_id = dd.CharField(max_length=200)

def sync_calendar_events(resource, sub, room, user):
    Event = rt.models.cal.Event
    def sync10(nextPageToken=None):
        events = resource.events().list(
            calendarId=sub.calendar.google_id, maxResults=10,
            syncToken=sub.sync_token, pageToken=nextPageToken).execute()
        sub.sync_token = events.get('nextSyncToken')

        if items := events['items']:
            for item in items:
                event = Event.insert_or_update_google_event(item, room, user)

        if next_page_token := events.get('nextPageToken'):
            sync10(next_page_token)

    sync10()
    sub.full_clean()
    sub.save()


def sync_user_calendar(user):
    gcal = get_resource(user)

    Calendar = rt.models.cal.Calendar
    CalendarSubscription = rt.models.google.CalendarSubscription
    Event = rt.models.cal.Event

    # Outward sync

    if not settings.SITE.is_demo_site:
        cal_res = gcal.calendars()

        Calendar.sync_deleted_records()
        Event.sync_deleted_records()

        for c in Calendar.get_outward_insert_update_queryset(user):
            c.insert_or_update_into_google(cal_res, user)

        ers = gcal.events()
        for e in Event.get_outward_insert_update_queryset(user):
            e.insert_or_update_into_google(ers, user)

    # Inward sync

    def sync10(nextPageToken=None):
        cals = gcal.calendarList().list(maxResults=10, syncToken=user.calendar_sync_token, showDeleted=True,
                                            showHidden=True, pageToken=nextPageToken).execute()
        user.calendar_sync_token = cals.get('nextSyncToken')

        for cal in cals.get("items", []):
            if deleted := cal.get("deleted", False):
                Calendar.delete_google_calendar(cal)
                continue
            calendar, room = Calendar.insert_or_update_google_calendar(cal, user)

            try:
                subscription = CalendarSubscription.objects.get(user=user, calendar=calendar)
            except CalendarSubscription.DoesNotExist:
                subscription = CalendarSubscription(user=user, calendar=calendar)
                ar = CalendarSubscription.get_default_table().request(user=user)
                subscription.full_clean()
                subscription.save_new_instance(ar)
            subscription.primary = cal.get("primary", False)
            subscription.access_role = cal.get("accessRole", "reader")
            subscription.full_clean()
            subscription.save()

            sync_calendar_events(gcal, subscription, room, user)

        if next_page_token := cals.get('nextPageToken'):
            sync10(next_page_token)

    sync10()
    user.full_clean()
    user.save()

    gcal.close()


class SynchronizeGoogle(dd.Action):
    help_text = _("Synchronize this database row with Google.")
    label = _("Sync Google Calendar")
    select_rows = False

    def run_from_ui(self, ar):
        sync_user_calendar(ar.get_user())
        ar.success()


dd.inject_action('users.User', synchronize_google=SynchronizeGoogle())

DELETED_EVENTS_META = {}
DELETED_CALENDARS_META = {}

@dd.receiver(dd.post_analyze)
def set_delete_signal_receivers(*args, **kwargs):
    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Event)
    def event_will_get_deleted(sender, instance, **kwargs):
        if instance.google_id and instance.synchronize_with_google():
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance.get_calendar()
            ).first()
            if sub is not None and (user := sub.user) is not None:
                DELETED_EVENTS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Event)
    def event_deleted(sender, instance, **kwargs):
        if user := DELETED_EVENTS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(event_id=instance.google_id, user=user,
                                                  calendar_id=instance.get_calendar().google_id)
            entry.full_clean()
            entry.save()
            del DELETED_EVENTS_META[instance.google_id]

    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Calendar)
    def calendar_will_get_deleted(sender, instance, **kwargs):
        if instance.google_id:
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance
            ).first()
            if sub is not None and (user := sub.user):
                DELETED_CALENDARS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Calendar)
    def calendar_deleted(sender, instance, **kwargs):
        if user := DELETED_CALENDARS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(calendar_id=instance.google_id, calendar=True, user=user)
            entry.full_clean()
            entry.save()
            del DELETED_CALENDARS_META[instance.google_id]
