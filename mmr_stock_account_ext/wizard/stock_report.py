# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round


class stock_report_line(models.TransientModel):
    _inherit = 'stock.report.line'

    invoice_date = fields.Date('Invoice Date', related="stock_move_id.picking_id.mmr_invoice_date")
