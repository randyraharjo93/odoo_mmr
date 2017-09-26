# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()
        for order in self:
            for purchase_line in order.order_line:
                if purchase_line.product_qty > 0:
                    purchase_price_plus15 = purchase_line.price_subtotal / purchase_line.product_qty + (purchase_line.price_subtotal / purchase_line.product_qty * 0.15)
                    if purchase_price_plus15 > purchase_line.product_id.lst_price:
                        purchase_line.product_id.lst_price = purchase_price_plus15
        return True

    @api.multi
    def button_confirm_with_notification(self):
        for order in self:
            need_notification = False
            for purchase_line in order.order_line:
                if purchase_line.product_qty > 0:
                    purchase_price_plus15 = purchase_line.price_subtotal / purchase_line.product_qty + (purchase_line.price_subtotal / purchase_line.product_qty * 0.15)
                    if purchase_price_plus15 > purchase_line.product_id.lst_price:
                        need_notification = True
            print need_notification
            if need_notification:
                return {
                    'name':_("Confirm Notification"),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'price.update.notification',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    }
            else:
                self.button_confirm()
        return True
