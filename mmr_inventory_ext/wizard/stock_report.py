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

        move_in_ids = Move.search(domain_move_in)
        move_out_ids = Move.search(domain_move_out)
        report_line_ids = []

        combined_sorted_move_ids = sorted((move_in_ids + move_out_ids).read(['date']), key=lambda k: k['date'])
        total_uom_qty = 0
        for move in combined_sorted_move_ids:
            move_id = Move.browse(move['id'])
            if move_id in move_in_ids:
                total_uom_qty += move_id.product_uom_qty
                report_line_ids.append((0, 0, {'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'date': move_id.date, 'in_qty': move_id.product_uom_qty, 'product_lot_id': move_id.restrict_lot_id, 'total_qty': total_uom_qty}))
            elif move_id in move_out_ids:
                total_uom_qty -= move_id.product_uom_qty
                report_line_ids.append((0, 0, {'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'date': move_id.date, 'out_qty': move_id.product_uom_qty, 'product_lot_id': move_id.restrict_lot_id, 'total_qty': total_uom_qty}))
        self.stock_report_line_ids = report_line_ids
        return True


class stock_report_line(models.TransientModel):
    _name = 'stock.report.line'
    _description = "Stock Report Line"

    stock_report_id = fields.Many2one("stock.report", "Stock Report")
    source = fields.Char("Source")
    date = fields.Datetime("Date")
    product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    product_lot_id = fields.Many2one('stock.production.lot', 'LOT / SN')
    in_qty = fields.Float('In', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    out_qty = fields.Float('Out', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty_lot = fields.Float('LOT / SN Total', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty = fields.Float('Total', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
