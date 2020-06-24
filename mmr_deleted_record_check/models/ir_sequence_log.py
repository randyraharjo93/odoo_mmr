# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class IrSequenceLog(models.Model):
    _name = "ir.sequence.log"

    name = fields.Char("Name")
    sequence_id = fields.Many2one("ir.sequence", "Sequence")
    sequence_date_range_id = fields.Many2one("ir.sequence.date_range", "Sequence Date Range")
    message = fields.Char("Log Message")
