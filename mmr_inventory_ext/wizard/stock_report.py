# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class stock_report(models.TransientModel):
    _name = 'stock.report'
    _description = "Stock Report"

    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date Start")
    product_id = fields.Many2one("product.product", "Product", domain="[('type','=','product')]")
    stock_report_line_ids = fields.One2many("stock.report.line", "stock_report_id", "Movement(s)")

    @api.onchange('date_start', 'date_end', 'product_id')
    def check(self):
        search_terms = []
        if self.product_id:
            search_terms.append(('product_id', '=', self.product_id.id))
        if self.date_start:
            search_terms.append(('in_date', '>=', self.date_start))
        if self.date_end:
            search_terms.append(('in_date', '<=', self.date_end))
        if search_terms:
            movement_ids = self.env['stock.quant'].search(search_terms)
            print (movement_ids.ids)
            for movement_id in movement_ids:
                print(movement_id)


class stock_report_line(models.TransientModel):
    _name = 'stock.report.line'
    _description = "Stock Report Line"

    stock_report_id = fields.Many2one("stock.report", "Stock Report")
    source = fields.Char("Source")
    date = fields.Date("Date")
    product_id = fields.Many2one("product.product", "Product")
    product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    product_lot_id = fields.Many2one('stock.production.lot', 'LOT / SN')
    in_qty = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    out_qty = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty_lot = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty = fields.Float('Quantity', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
