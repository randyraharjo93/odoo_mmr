# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class stock_report(models.TransientModel):
    _name = 'stock.report'
    _description = "Stock Report"

    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")
    product_id = fields.Many2one("product.product", "Product", domain="[('type','=','product')]")
    stock_report_line_ids = fields.One2many("stock.report.line", "stock_report_id", "Movement(s)")

    @api.onchange('date_start', 'date_end', 'product_id')
    def check(self):
        if self.product_id:
            # print(self._compute_quantities_dict(self.product_id, self.date_start, self.date_end))
            print(self._compute_quantities_dict(self.product_id, self.date_start, self.date_end))

    @api.multi
    def _compute_quantities_dict(self, product_id, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product_id._get_domain_locations()

        domain_move_in = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_in_loc
        domain_move_out = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_out_loc

        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        Move = self.env['stock.move']

        print("LEARN------------------------")
        print(domain_move_in)
        print(Move.search(domain_move_in))
        # print(domain_move_out)
        # print(Move.search(domain_move_out))
        print([move.quant_ids.ids for move in Move.search(domain_move_in)])

        return True


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
