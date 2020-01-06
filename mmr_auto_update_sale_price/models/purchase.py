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
                base_uom_id = purchase_line.product_uom.search([('category_id', '=', purchase_line.product_uom.category_id.id), ('uom_type', '=', 'reference')])
                if base_uom_id:
                    if purchase_line.product_qty > 0:
                        real_qty = purchase_line.product_uom._compute_quantity(purchase_line.product_qty, base_uom_id)
                        unit_price = purchase_line.price_unit
                        if real_qty != purchase_line.product_qty:
                            unit_price = purchase_line.price_unit / real_qty
                        discounted_unit_price = unit_price - (unit_price * purchase_line.discount / 100)
                        purchase_price_plus15 = discounted_unit_price + (discounted_unit_price * 0.15)
                        if purchase_price_plus15 > purchase_line.product_id.lst_price:
                            purchase_line.product_id.lst_price = purchase_price_plus15
        return True

    @api.multi
    def button_confirm_with_notification(self):
        for order in self:
            need_notification = False
            for purchase_line in order.order_line:
                base_uom_id = purchase_line.product_uom.search([('category_id', '=', purchase_line.product_uom.category_id.id), ('uom_type', '=', 'reference')])
                if base_uom_id:
                    if purchase_line.product_qty > 0:
                        real_qty = purchase_line.product_uom._compute_quantity(purchase_line.product_qty, base_uom_id)
                        unit_price = purchase_line.price_unit
                        if real_qty != purchase_line.product_qty:
                            unit_price = purchase_line.price_unit / real_qty
                        discounted_unit_price = unit_price - (unit_price * purchase_line.discount / 100)
                        purchase_price_plus15 = discounted_unit_price + (discounted_unit_price * 0.15)
                        if purchase_price_plus15 > purchase_line.product_id.lst_price:
                            need_notification = True
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
