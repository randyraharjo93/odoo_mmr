# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_order_line_history_ids = fields.Many2many("sale.order.line", "sale_order_line_sale_order_line_rel", "order_line_1_id", "order_line_2_id", string="History")
    date_order = fields.Datetime("Order Data", related="order_id.date_order")

    @api.onchange("product_id", "order_partner_id")
    def _onchange_sale_order_line(self):
        order_line_ids = self.search([('product_id', '=', self.product_id.id), ('order_partner_id', '=', self.order_partner_id.id)], order="create_date desc")
        self.sale_order_line_history_ids = order_line_ids
