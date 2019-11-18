# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class stock_quant_change(models.TransientModel):
    _name = 'stock.quant.change'
    _description = "Stock Quant Change"

    new_value = fields.Float('New Value')

    def button_change_value(self):
        stock_quant_id = self.env['stock.quant'].browse(self.env.context.get('active_ids'))
        stock_quant_id.cost = self.new_value / stock_quant_id.qty
