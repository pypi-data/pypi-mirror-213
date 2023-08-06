# -*- coding: UTF-8 -*-
# Copyright 2019-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from decimal import Decimal
from etgen.html import E, join_elems, tostring

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.text import format_lazy

from lino.api import dd, rt
from lino.utils.dates import DateRangeValue

from lino.mixins import ProjectRelated
from lino.mixins.ref import Referrable
from lino.mixins.human import parse_name
from lino.mixins.duplicable import Duplicable
from lino.mixins.periods import DateRange
# from lino.mixins.registrable import Registrable
from lino_xl.lib.ledger.utils import ZERO, ONE
from lino_xl.lib.ledger.choicelists import VoucherStates
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_xl.lib.excerpts.mixins import ExcerptTitle
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.printing.mixins import Printable
# from lino.modlib.printing.utils import PrintableObject
# from lino_xl.lib.cal.mixins import Reservation
from lino_xl.lib.cal.utils import day_and_month
from lino_xl.lib.cal.mixins import EventGenerator
from lino_xl.lib.invoicing.mixins import InvoiceGenerator, Periodicities
from lino_xl.lib.contacts.mixins import PartnerRelated
from lino_xl.lib.ledger.models import RegistrableVoucher
from lino_xl.lib.ledger.mixins import SequencedVoucherItem
from lino_xl.lib.sales.mixins import SalesPrintable, ProductDocItem
from lino_xl.lib.excerpts.mixins import Certifiable


class Subscription(RegistrableVoucher, PartnerRelated, SalesPrintable,
        Duplicable, InvoiceGenerator, Referrable):

    class Meta:
        app_label = 'subscriptions'
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _('Subscriptions')

    hide_editable_number = False

    quick_search_fields = "ref subject"

    state = VoucherStates.field(default='draft')
    # subject = models.CharField(_("Our reference"), max_length=200, blank=True)
    # description = dd.TextField(_("Description"), blank=True)
    start_date = models.DateField(_("Start date"), blank=True, null=True)
    end_date = models.DateField(_("End date"), blank=True, null=True)
    subscription_periodicity = Periodicities.field(blank=True, null=True)
    invoiceable_product = dd.ForeignKey('products.Product', blank=True, null=True)

    # def full_clean(self, *args, **kwargs):
    #     # if self.entry_date is None:
    #     #     self.entry_date = dd.today()
    #     if self.partner is None:
    #         raise Warning(_("Either company or person must be given."))
    #     super().full_clean(*args, **kwargs)

    def __str__(self):
        p = self.company or self.person
        if self.ref and p:
            return "{} {} ({})".format(self.ref, p, super().__str__())
        elif self.ref:
            return "{} ({})".format(self.ref, super().__str__())
        return super().__str__()

    def get_wanted_movements(self):
        return []

    # @classmethod
    # def get_registrable_fields(cls, site):
    #     for f in super().get_registrable_fields(site):
    #         yield f
    #     yield 'name'

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        # pre-select which subscriptions may potentially generate an invoice for
        # the given plan.

        qs = super().get_generators_for_plan(plan, partner)

        # if plan.invoicing_area is None:
        #     raise Exception("20221217")

        if plan.order is None:
            qs = qs.exclude(state=VoucherStates.cancelled)
            qs = qs.exclude(state=VoucherStates.draft)
        elif issubclass(dd.plugins.invoicing.order_model, cls):
            qs = qs.filter(id=plan.order.id)
        else:
            raise Exception("20210731 {}".format(dd.plugins.invoicing.order_model))

        if partner is None:
            partner = plan.partner

        if partner is not None:
            fldname = cls.get_partner_filter_field(partner)
            qs = cls.filter_by_invoice_recipient(qs, partner, fldname)

        # dd.logger.info("20200518 %s (%d rows)", qs.query, qs.count())
        return qs.order_by('id')

    # def get_invoice_items(self, info, invoice, ar):
    #     # dd.logger.info("20181116a %s", self)
    #     # print("20221222 get_invoice_items()", self.items.all())
    #     if info.asset_to_buy is not None:
    #         kwargs = dict(
    #             # 20210804 invoiceable=self,
    #             product=self.get_invoiceable_product(self.entry_date),
    #             unit_price=self.total_base)
    #         i = invoice.add_voucher_item(**kwargs)
    #         i.product_changed(ar)
    #         i.unit_price_changed(ar)
    #         # i.reset_totals(ar)
    #         if i.total_incl is None:
    #             raise Exception("20210731 invoice item without amount:", i.__class__, i)
    #         yield i

    def get_invoice_items(self, info, invoice, ar):
        # dd.logger.info("20181116a %s", self)
        # print("20221222 get_invoice_items()", self.items.all())
        if info.asset_to_buy is None:
            return
        for i in super().get_invoice_items(info, invoice, ar):
            # print("20210731 a", i)
            yield i
        # print("20221222 asset_to_buy is", info.number_of_events, info.asset_to_buy)
        # if info.number_of_events is None:
        for oi in self.items.all():
            kwargs = dict(
                # 20210804 invoiceable=self,
                product=oi.product,
                discount=oi.discount,
                unit_price=oi.unit_price,
                qty=oi.qty)
            i = invoice.add_voucher_item(**kwargs)
            i.product_changed(ar)
            # i.reset_totals(ar)
            # if i.total_incl is None:
            #     print("20210731 invoice item without amount:", i.__class__, i)
            yield i


    def get_invoiceable_partner(self):
        return self.partner

    def get_invoiceable_product(self, max_date=None):
        return self.invoiceable_product

    # def get_invoiceable_qty(self):
    #     return self.default_invoiceable_qty

    # def get_invoicing_pass_type(self, product=None):
    #     if product is not None:
    #         return product.tariff
    #     return None

    def get_invoiceable_start_date(self, max_date):
        return self.start_date

    def get_invoiceable_end_date(self):
        return self.end_date

    def get_invoicing_periodicity(self, product):
        return self.subscription_periodicity

    def get_invoiceable_title(self, number=None):
        return str(self)

# dd.update_field(Subscription, "ref", verbose_name=_("Nickname"))


class SubscriptionItem(SequencedVoucherItem):
    class Meta:
        app_label = 'subscriptions'
        abstract = dd.is_abstract_model(__name__, 'SubscriptionItem')
        verbose_name = _("Subscription item")
        verbose_name_plural = _("Subscription items")

    allow_cascaded_delete = 'voucher'

    voucher = dd.ForeignKey('subscriptions.Subscription', related_name='items')
    product = dd.ForeignKey('products.Product', blank=True, null=True)
    qty = dd.QuantityField(_("Quantity"), blank=True, null=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)
    unit_price = dd.PriceField(_("Unit price"), blank=True, null=True)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)


from .ui import *
