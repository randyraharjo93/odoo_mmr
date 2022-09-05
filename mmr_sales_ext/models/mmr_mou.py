# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import logging
from datetime import datetime, date, timedelta

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
    reminder = fields.Selection([
        ('open', 'Open'),
        ('3m', 'Close in 3 Months'),
        ('2m', 'Close in 2 Months'),
        ('1m', 'Close in 1 Months'),
        ('close', 'Closed')], compute="_compute_get_reminder")

    def _compute_get_reminder(self):
        for mou in self:
            if not mou.date_end or datetime.strptime(mou.date_end, '%Y-%m-%d') >= (datetime.today() + timedelta(90)):
                mou.reminder = 'open'
            elif datetime.strptime(mou.date_end, '%Y-%m-%d') < (datetime.today() + timedelta(90)) and datetime.strptime(mou.date_end, '%Y-%m-%d') >= (datetime.today() + timedelta(60)):
                mou.reminder = '3m'
            elif datetime.strptime(mou.date_end, '%Y-%m-%d') < (datetime.today() + timedelta(60)) and datetime.strptime(mou.date_end, '%Y-%m-%d') >= (datetime.today() + timedelta(30)):
                mou.reminder = '2m'
            elif datetime.strptime(mou.date_end, '%Y-%m-%d') < (datetime.today() + timedelta(30)) and datetime.strptime(mou.date_end, '%Y-%m-%d') >= (datetime.today() + timedelta(0)):
                mou.reminder = '1m'
            else:
                mou.reminder = 'close'
