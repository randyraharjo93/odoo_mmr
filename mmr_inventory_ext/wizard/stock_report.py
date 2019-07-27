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
    def onchange_stock_card(self):
        if self.product_id:
            self._compute_quantities_dict(self.product_id, self.date_start, self.date_end)

    @api.multi
    def _compute_quantities_dict(self, product_id, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product_id._get_domain_locations()

        domain_move_in = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_in_loc
        domain_move_out = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_out_loc

        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]

            # If there is From, Means I want Starting Value
            domain_move_in_start_value = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_in_loc + [('date', '<', from_date)]
            domain_move_out_start_value = [('state', '=', 'done'), ('product_id', 'in', [product_id.id])] + domain_move_out_loc + [('date', '<', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        Move = self.env['stock.move']

        move_in_ids = Move.search(domain_move_in)
        move_out_ids = Move.search(domain_move_out)
        report_line_ids = []

        if from_date:
            move_in_start_ids = Move.search(domain_move_in_start_value)
            move_out_start_ids = Move.search(domain_move_out_start_value)
            combined_sorted_starting_move_ids = sorted((move_in_start_ids + move_out_start_ids).read(['date']), key=lambda k: k['date'])
            total_start_uom_qty = 0
            total_start_value = 0
            for start_move in combined_sorted_starting_move_ids:
                move_id = Move.browse(start_move['id'])
                if move_id in move_in_start_ids:
                    total_start_uom_qty += move_id.product_uom_qty
                    value = 0
                    if move_id.price_unit:
                        value = move_id.price_unit * move_id.product_uom_qty
                    else:
                        value = sum(quant.inventory_value for quant in move_id.quant_ids)
                    total_start_value += value
                elif move_id in move_out_start_ids:
                    total_start_uom_qty -= move_id.product_uom_qty
                    value = 0
                    if move_id.price_unit:
                        value = move_id.price_unit * move_id.product_uom_qty
                    else:
                        value = sum(quant.inventory_value for quant in move_id.quant_ids)
                    total_start_value -= value
            if total_start_uom_qty > 0:
                report_line_ids.append((0, 0, {'source': "Starting Value", 'date': move_id.date, 'in_qty': total_start_uom_qty, 'total_qty': total_start_uom_qty, 'value': total_start_value, 'total_value': total_start_value}))

        combined_sorted_move_ids = sorted((move_in_ids + move_out_ids).read(['date']), key=lambda k: k['date'])
        if from_date and total_start_uom_qty:
            total_uom_qty = total_start_uom_qty
            total_value = total_start_value
        else:
            total_uom_qty = 0
            total_value = 0
        for move in combined_sorted_move_ids:
            move_id = Move.browse(move['id'])
            if move_id in move_in_ids:
                total_uom_qty += move_id.product_uom_qty
                value = 0
                if move_id.price_unit:
                    value = move_id.price_unit * move_id.product_uom_qty
                else:
                    value = sum(quant.inventory_value for quant in move_id.quant_ids)
                total_value += value
                if move_id.linked_move_operation_ids:
                    for linked_move_operation_id in move_id.linked_move_operation_ids:
                        if len(linked_move_operation_id.operation_id.pack_lot_ids) > 0:
                            for pack_lot_id in linked_move_operation_id.operation_id.pack_lot_ids:
                                report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'in_qty': pack_lot_id.qty, 'product_lot_id': pack_lot_id.lot_id, 'total_qty': total_uom_qty, 'value': move_id.price_unit * pack_lot_id.qty, 'total_value': total_value}))
                        else:
                            report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'in_qty': linked_move_operation_id.qty, 'total_qty': total_uom_qty, 'value': move_id.price_unit * linked_move_operation_id.qty, 'total_value': total_value}))
                else:
                    report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'in_qty': move_id.product_uom_qty, 'product_lot_id': move_id.lot_ids and move_id.lot_ids[0], 'total_qty': total_uom_qty, 'value': value, 'total_value': total_value}))

            elif move_id in move_out_ids:
                total_uom_qty -= move_id.product_uom_qty
                value = 0
                if move_id.price_unit:
                    value = move_id.price_unit * move_id.product_uom_qty
                else:
                    value = sum(quant.inventory_value for quant in move_id.quant_ids)
                total_value -= value
                if move_id.linked_move_operation_ids:
                    for linked_move_operation_id in move_id.linked_move_operation_ids:
                        if len(linked_move_operation_id.operation_id.pack_lot_ids) > 0:
                            for pack_lot_id in linked_move_operation_id.operation_id.pack_lot_ids:
                                report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'out_qty': pack_lot_id.qty, 'product_lot_id': pack_lot_id.lot_id, 'total_qty': total_uom_qty, 'value': move_id.price_unit * pack_lot_id.qty, 'total_value': total_value}))
                        else:
                            report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'out_qty': linked_move_operation_id.qty, 'total_qty': total_uom_qty, 'value': move_id.price_unit * linked_move_operation_id.qty, 'total_value': total_value}))
                else:
                    report_line_ids.append((0, 0, {'stock_move_id': move_id, 'partner_id': move_id.partner_id or move_id.picking_id.partner_id, 'source': move_id.origin or move_id.picking_id.origin or move_id.picking_id.name or "Unidentified", 'product_uom_id': move_id.product_uom, 'date': move_id.date, 'out_qty': move_id.product_uom_qty, 'product_lot_id': move_id.lot_ids and move_id.lot_ids[0], 'total_qty': total_uom_qty, 'value': value, 'total_value': total_value}))

        self.stock_report_line_ids = report_line_ids
        return True


class stock_report_line(models.TransientModel):
    _name = 'stock.report.line'
    _description = "Stock Report Line"

    stock_report_id = fields.Many2one("stock.report", "Stock Report")
    partner_id = fields.Many2one('res.partner', 'Partner')
    stock_move_id = fields.Many2one('stock.move', 'Move')
    source = fields.Char("Source")
    date = fields.Datetime("Date")
    product_uom_id = fields.Many2one('product.uom', 'Unit of Measure')
    product_lot_id = fields.Many2one('stock.production.lot', 'LOT / SN')
    in_qty = fields.Float('In', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    out_qty = fields.Float('Out', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty_lot = fields.Float('LOT / SN Total', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    total_qty = fields.Float('Total Qty', default=1.0, digits=dp.get_precision('Product Unit of Measure'))
    value = fields.Float("Value")
    total_value = fields.Float("Total Value")
