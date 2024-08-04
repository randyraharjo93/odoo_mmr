# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_order_line_history_ids = fields.Many2many("sale.order.line", "sale_order_line_sale_order_line_rel", "order_line_1_id", "order_line_2_id", string="History")
    date_order = fields.Datetime("Order Data", related="order_id.date_order")
    warning = fields.Text("Price Warning")

    @api.onchange("product_id", "price_unit", "order_partner_id")
    def _onchange_sale_order_line(self):
        self.warning = '/'
        order_line_ids = self.search([('product_id', '=', self.product_id.id), ('order_partner_id', '=', self.order_partner_id.id), ('state', '=', 'sale')], order="create_date desc")
        self.sale_order_line_history_ids = order_line_ids
        if order_line_ids:
            self.price_unit = order_line_ids[0].price_unit
            if tools.float_compare(order_line_ids[0].price_unit, self.price_unit, precision_digits=2) != 0:
                self.warning = 'Unit Price difference than last unit price'
