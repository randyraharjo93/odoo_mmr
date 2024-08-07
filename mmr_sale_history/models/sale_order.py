# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_order_line_history_ids = fields.Many2many("sale.order.line", "sale_order_line_sale_order_line_rel", "order_line_1_id", "order_line_2_id", string="History")
    date_order = fields.Datetime("Order Data", related="order_id.date_order")
    warning = fields.Text("Price Warning")
    use_last_price = fields.Boolean("Use Last Price")

    @api.onchange("product_id", "order_partner_id")
    def _onchange_sale_order_line(self):
        order_line_ids = self.search([('product_id', '=', self.product_id.id), ('order_partner_id', '=', self.order_partner_id.id), ('state', '=', 'sale')], order="create_date desc")
        self.sale_order_line_history_ids = order_line_ids
        self.use_last_price = False

    @api.onchange("price_unit", "sale_order_line_history_ids", "discount")
    def _onchange_price(self):
        self.warning = '/'
        if self.sale_order_line_history_ids:
            if tools.float_compare(self.sale_order_line_history_ids[0].price_unit, self.price_unit, precision_digits=2) != 0:
                self.warning = 'Unit Price difference than last unit price'
            if tools.float_compare(self.sale_order_line_history_ids[0].discount, self.discount, precision_digits=2) != 0:
                self.warning = 'Discount difference than last discount'
            if tools.float_compare(self.sale_order_line_history_ids[0].price_unit, self.price_unit, precision_digits=2) != 0 and tools.float_compare(self.sale_order_line_history_ids[0].discount, self.discount, precision_digits=2) != 0:
                self.warning = 'Unit Price difference than last unit price and Discount difference than last discount'

    @api.onchange("price_unit", "use_last_price", "discount")
    def _onchange_last_price(self):
        if self.use_last_price and self.sale_order_line_history_ids:
            self.price_unit = self.sale_order_line_history_ids[0].price_unit
            self.discount = self.sale_order_line_history_ids[0].discount
