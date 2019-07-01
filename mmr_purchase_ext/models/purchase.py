# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            # Don't show Price for normal purchase user
            if po.amount_total and self.user_has_groups("purchase.group_purchase_manager"):
                name += ': ' + formatLang(self.env, po.amount_total, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result

    filtered_message_ids = fields.Many2many("mail.message", compute="_get_save_message_ids")

    @api.one
    @api.depends('message_ids')
    def _get_save_message_ids(self):
        if self.message_ids:
            message_ids = []
            for message_id in self.message_ids:
                if not message_id.sudo().tracking_value_ids:
                    message_ids.append(message_id.id)
            self.sudo().filtered_message_ids = [(6, 0, message_ids)]

    @api.model
    def create(self, vals):
        result = super(PurchaseOrder, self).create(vals)
        # MMR Special Prefix
        # How to:
        # Put prefix "|%(year)s/%(month)s/%(day)s/"
        if len(result.name.split('|')) > 1:
            name_without_split = result.name.replace("|", "")
            prefix_name = (result.company_id.partner_id.ref or "") + "/" + (result.partner_id.ref or "") + "/"
            result.name = prefix_name + name_without_split
        return result

    @api.multi
    def write(self, vals):
        result = super(PurchaseOrder, self).write(vals)
        # MMR Special Prefix
        # How to:
        # Put prefix "|%(year)s/%(month)s/%(day)s/"
        if ('company_id' in vals or 'partner_id' in vals) and self.name and len(self.name.split('/')) == 6:
            name_split = self.name.split('/')
            prefix_name = (self.company_id.partner_id.ref or "") + "/" + (self.partner_id.ref or "") + "/"
            self.name = prefix_name + name_split[2] + "/" + name_split[3] + "/" + name_split[4] + "/" + name_split[5]
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return

        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        if not seller:
            # If no Seller default is 7
            date_order = self.order_id.date_order
            if date_order:
                self.date_planned = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(days=seller.delay if seller else 7)
            else:
                self.date_planned = datetime.today() + relativedelta(days=seller.delay if seller else 7)
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id.compute(price_unit, self.order_id.currency_id)

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit