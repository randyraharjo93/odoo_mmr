# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    purchase_order_line_history_ids = fields.Many2many("purchase.order.line", "purchase_order_line_purchase_order_line_rel", "order_line_1_id", "order_line_2_id", string="History")
    date_order = fields.Datetime("Order Data", related="order_id.date_order")

    @api.onchange("product_id", "partner_id", "include_group")
    def _onchange_purchase_order_line(self):
        order_line_ids = self.search([('product_id', '=', self.product_id.id), ('partner_id', '=', self.partner_id.id)], order="create_date desc")
        self.purchase_order_line_history_ids = order_line_ids
