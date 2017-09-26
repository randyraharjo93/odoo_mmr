# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class price_update_notification(models.TransientModel):
    _name = 'price.update.notification'
    _description = "Price Update Notification"

    def _get_default_notification(self):
        notification = ""
        for purchase_line in self.env['purchase.order'].browse(self._context['active_id']).order_line:
            if purchase_line.product_qty > 0:
                purchase_price_plus15 = purchase_line.price_subtotal / purchase_line.product_qty + (purchase_line.price_subtotal / purchase_line.product_qty * 0.15)
                if purchase_price_plus15 > purchase_line.product_id.lst_price:
                    notification += "Sale Price of Product : " + purchase_line.product_id.display_name + " Will be updated to : " + str(purchase_price_plus15) + " (Old Price : " + str(purchase_line.product_id.lst_price) + ")\n"
        return notification

    notification = fields.Text("Notification", default=_get_default_notification, readonly=True)

    @api.multi
    def confirm_sale(self):
        self.env['purchase.order'].browse(self._context['active_id']).button_confirm()
