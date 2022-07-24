# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import logging

_logger = logging.getLogger(__name__)


class MMRMoU(models.Model):
    _name = "mmr.mou"

    name = fields.Char("Name", required=True, help='Memorandum of Understanding Name')
    partner_id = fields.Many2one('res.partner', string="Customer")
    tnc = fields.Text("Terms and Conditions")
    expected_value = fields.Monetary("Expected Value", track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id.id, required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id, required=True)
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")
