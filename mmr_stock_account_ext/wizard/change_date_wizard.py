# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class MMRChangeDate(models.TransientModel):
    _name = "mmr.change.date"

    new_date = fields.Date('New Date')

    @api.multi
    def do_change_date(self):
        stock_picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id', False))
        for account_move_id in stock_picking_id.mmr_account_move_ids:
            account_move_id.button_cancel()
            account_move_id.date = self.new_date
            for account_move_line in account_move_id.line_ids:
                account_move_line.date = self.new_date
            account_move_id.post()
