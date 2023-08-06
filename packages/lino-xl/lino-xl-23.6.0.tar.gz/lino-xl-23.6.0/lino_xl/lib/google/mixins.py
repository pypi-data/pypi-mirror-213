# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
import logging
from dateutil.parser import parse
from django.db import models
from django.utils import timezone
from lino.mixins import Modified
from lino.api import dd, rt, _

from .choicelists import EntryStates, GuestStates, google_status

logger = logging.getLogger(__name__)


if dd.is_installed('google'):
    try:
        from googleapiclient.errors import HttpError
    except ImportError:
        HttpError = None


class GoogleSynchronized(dd.Model):
    class Meta:
        abstract = True

    if dd.is_installed('google'):
        google_id = dd.CharField(max_length=200, verbose_name=_('Google resource ID'), blank=True)

        def synchronize_with_google(self, user=None) -> bool:
            return True


class GoogleCalendarSynchronized(GoogleSynchronized):
    class Meta:
        abstract = True

    if dd.is_installed('google'):

        modified = models.DateTimeField(_("Modified"), editable=False, null=True)

        def insert_or_update_into_google(self, crs, user):
            body = {
                'summary': self.name,
                'description': self.description,
                'timeZone': user.time_zone.text
            }
            if self.google_id:
                c = crs.get(calendarId=self.google_id).execute()
                if c.get('timeZone') is not None:
                    body.pop('timeZone')
                crs.update(calendarId=self.google_id, body=body).execute()
            else:
                c = crs.insert(body=body).execute()
                self.google_id = c.get('id')
                self.full_clean()
                self.save()

        @classmethod
        def get_outward_insert_update_queryset(cls, user):
            return cls.objects.annotate(subscribed=models.Case(
                models.When(models.Exists(
                    rt.models.google.CalendarSubscription.objects.filter(
                        calendar__pk=models.OuterRef("pk"), user=user
                    ),
                ), then=models.Value(True)),
                output_field=models.BooleanField(),
                default=models.Value(False)
            )).filter(models.Q(google_id='') | models.Q(modified__gte=user.modified), subscribed=True)

        @classmethod
        def delete_google_calendar(cls, cal):
            try:
                gid = cal["id"]
                calendar = cls.objects.get(google_id=gid)
                calendar.delete()
                rt.models.google.DeletedEntry.objects.filter(calendar=True, calendar_id=gid).delete()
            except cls.DoesNotExist:
                pass

        @classmethod
        def sync_deleted_records(cls):
            get_res = rt.models.google.get_resource
            users = {}
            for obj in rt.models.google.DeletedEntry.objects.filter(calendar=True):
                if obj.user.pk not in users:
                    users[obj.user.pk] = get_res(obj.user).calendars()
                crs = users[obj.user.pk]
                crs.delete(calendarId=obj.calendar_id).execute()
            for res in users.values():
                res.close()

        @classmethod
        def insert_or_update_google_calendar(cls, cal: dict, user=None):
            try:
                calendar = cls.objects.get(google_id=cal["id"])
                if name := cal.get('summary'):
                    calendar.name = name
                if description := cal.get('description'):
                    calendar.description = description
            except cls.DoesNotExist:
                calendar = cls(
                    google_id=cal["id"],
                    name=cal.get("summary", ""),
                    description=cal.get("description", "")
                )

            if color := cal.get('colorId'):
                calendar.color = color
            calendar.full_clean()
            if calendar.pk is None:
                ar = cls.get_default_table().request(user=user)
                calendar.save_new_instance(ar)
            else:
                calendar.save()

            Room = rt.models.cal.Room
            room_desc = cal.get("location") or cal.get("description", "")
            room = calendar.room_calendars.filter(description=room_desc).first()
            if room is None:
                room = Room(
                    name=cal.get("summary", ""),
                    description=room_desc,
                    calendar=calendar
                )
                room.full_clean()
                ar = Room.get_default_table().request(user=user)
                room.save_new_instance(ar)

            return calendar, room


class GoogleCalendarEventSynchronized(GoogleSynchronized):
    class Meta:
        abstract = True

    if dd.is_installed('google'):

        def synchronize_with_google(self, user=None) -> bool:
            if self.end_time is None and self.end_date is None:
                return False
            if not (calendar := self.get_calendar()):
                return False
            if user is not None:
                return rt.models.google.CalendarSubscription.objects.filter(calendar=calendar, user=user).exists()
            return super().synchronize_with_google()

        @classmethod
        def delete_google_event(cls, event: dict):
            try:
                eid = event["id"]
                e = cls.objects.get(google_id=eid)
                e.delete()
                rt.models.google.DeletedEntry.objects.filter(calendar=False, event_id=eid,
                                                             calendar_id=e.get_calendar().google_id).delete()
            except Calendar.DoesNotExist:
                pass

        @classmethod
        def sync_deleted_records(cls):
            get_res = rt.models.google.get_resource
            users = {}
            for obj in rt.models.google.DeletedEntry.objects.select_related('user').filter(calendar=False):
                if obj.user.pk not in users:
                    users[obj.user.pk] = get_res(obj.user).events()
                crs = users[obj.user.pk]
                crs.delete(calendarId=obj.calendar_id, eventId=obj.event_id).execute()
            for res in users.values():
                res.close()

        @classmethod
        def get_outward_insert_update_queryset(cls, user):
            excludes = []
            for sub in user.google_calendarsubscription_set_by_user.filter(
                    models.Q(access_role='writer') | models.Q(access_role='owner')):
                modt = sub.modified
                cal = sub.calendar
                for e in cls.objects.filter(models.Q(google_id='') | models.Q(modified__gte=modt)).exclude(
                        pk__in=excludes):
                    if e.synchronize_with_google(user) and e.get_calendar() == cal:
                        excludes.append(e.pk)
                        yield e

        def insert_or_update_into_google(self, ers, user):
            body = {
                'summary': self.summary,
                'description': self.description,
                'sequence': self.sequence
            }

            if self.start_time:
                body['start'] = {'dateTime': self.get_datetime('start').isoformat()}
            elif self.start_date:
                body['start'] = {'date': self.start_date.isoformat()}
            # TODO: what's originalStart

            if self.end_time:
                body['end'] = {'dateTime': self.get_datetime('end').isoformat()}
            elif self.end_date:
                body['end'] = {'date': self.end_date.isoformat()}

            attendees = []
            for guest in self.guest_set.all():
                if email := guest.partner.email:
                    attendee = {'email': email}
                    if status := google_status(guest.state):
                        attendee['responseStatus'] = status
                    attendees.append(attendee)
            if attendees:
                body['attendees'] = attendees
            cal = self.get_calendar()
            if self.google_id:
                ers.update(calendarId=cal.google_id, eventId=self.google_id, body=body).execute()
            else:
                e = ers.insert(calendarId=cal.google_id, body=body).execute()
                self.google_id = e['id']
                self.full_clean()
                self.save()

        @classmethod
        def insert_or_update_google_event(cls, event: dict, room, user):
            try:
                e = cls.objects.get(google_id=event['id'])
            except cls.DoesNotExist:
                e = cls(google_id=event['id'])
            if state := EntryStates.get_by_name(event.get('status', ''), None):
                if e.state is not None and google_status(e.state) != state:
                    e.state = state

            e.summary = event.get('summary', "")  # The title of the event
            e.description = event.get('description', "")
            e.sequence = event.get('sequence', 0)

            if e.room is None:
                e.room = room

            if location := event.get('location'):
                if location != e.room.description:
                    Room = room.__class__
                    try:
                        room = Room.objects.get(description=location, calendar=room.calendar)
                    except Room.DoesNotExist:
                        room = e.room
                        room.pk = None
                        room.description = location
                        ar = Room.get_default_table().request(user=user)
                        room.full_clean()
                        room.save_new_instance(ar)
                    e.room = room
                    # TODO: clear up unused rooms

            def resolve_datetime(stamp, tz=None):
                dt = parse(stamp)
                if timezone.is_aware(dt):
                    return dt
                if tz is not None:
                    with timezone.override(tz):
                        return timezone.make_aware(dt)
                return timezone.make_aware(dt)

            def resolve_date_time(stamp, tz=None):
                dt = resolve_datetime(stamp, tz)
                return dt.date(), dt.time()

            if start := event.get('start'):
                if dateTime := start.get('dateTime'):
                    e.start_date, e.start_time = resolve_date_time(dateTime)
                else:
                    e.start_date = datetime.date(
                        *map(int, start['date'].split('-')))
            elif originalStart := event.get('originalStartTime'):
                if dateTime := originalStart.get('dateTime'):
                    e.start_date, e.start_time = resolve_date_time(dateTime)
                else:
                    e.start_date = datetime.date(
                        *map(int, originalStart['date'].split('-')))

            if end := event.get('end'):
                if dateTime := end.get('dateTime'):
                    e.end_date, e.end_time = resolve_date_time(dateTime)
                else:
                    e.end_date = datetime.date(
                        *map(int, end['date'].split('-')))

            author = None
            if creator := event.get('creator'):
                author = rt.models.users.User.objects.filter(email=creator['email']).first()
            if author is not None:
                e.user = author
            if e.user is None:
                e.user = user
            e.full_clean()
            if e.pk is None:
                ar = cls.get_default_table().request(user=user)
                e.save_new_instance(ar)
            else:
                e.save()

            if attendees := event.get('attendees'):
                # TODO: how about the removed attendees? There should be a definitive method to figure out
                #  which are Guest from google and which are lino native
                for attendee in attendees:
                    if attendee.get("organizer", False):
                        continue
                    if guest_email := attendee.get("email") is not None:
                        Partner = dd.resolve_model(dd.plugins.cal.partner_model)
                        partners = Partner.objects.filter(email=guest_email)
                        partner = None
                        if partners.count() >= 1:
                            partner = partners.filter(user__isnull=False).first()
                            if partner is None:
                                partner = partners[0]
                        if partner is not None:
                            Guest = rt.models.cal.Guest
                            try:
                                guest = Guest.objects.get(event=e, partner=partner)
                            except Guest.DoesNotExist:
                                guest = Guest(event=e, partner=partner)
                            if state := GuestStates.get_by_name(attendee.get("responseStatus", ''), None):
                                if guest.state is not None and google_status(guest.state) != state:
                                    guest.state = state
                            guest.full_clean()
                            if guest.pk is None:
                                ar = Guest.get_default_table().request(user=user)
                                guest.save_new_instance(ar)
                            else:
                                guest.save()

            return e


class GooglePeopleSynchronized(GoogleSynchronized):
    class Meta:
        abstract = True

    if dd.is_installed('google'):

        def save(self, *args, **kw):
            if self.synchronize_with_google():
                if not self.google_resourceName and self.name:
                    body = {'names': [
                        {'displayName': self.name, "givenName": self.last_name, "familyName": self.first_name}]}
                    if self.email:
                        body['emailAddresses'] = [{'value': self.email, 'type': 'work'}]
                    if dd.is_installed('phones'):
                        body.update(
                            {'PhoneNumber': [{'value': self.phone, 'type': 'main'},
                                             {'value': self.gsm, 'type': 'mobile'}]})
                    try:
                        results = service.people().createContact(body=body).execute()
                        if results and results.get('resourceName', False):
                            self.google_resourceName = results.get('resourceName', False)
                            self.google_contactID = results.get('resourceName', False).split('/')[1]
                    except HttpError as e:
                        print(e.content)
                elif self.google_resourceName:
                    try:
                        contactToUpdate = service.people().get(resourceName=self.google_resourceName,
                                                               personFields='names,emailAddresses').execute()
                        contactToUpdate['names'] = [
                            {'displayName': self.name, "givenName": self.last_name,
                             "familyName": self.first_name}]
                        service.people().updateContact(resourceName=self.google_resourceName,
                                                       updatePersonFields='names,emailAddresses',
                                                       body=contactToUpdate).execute()
                    except HttpError as e:
                        print(e.content)
            res = super(GooglePeople, self).save(*args, **kw)
            return res
