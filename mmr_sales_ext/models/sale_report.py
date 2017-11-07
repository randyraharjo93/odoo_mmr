# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    mmr_code_p = fields.Boolean(string='Code P', readonly=True)
    mmr_fee = fields.Float("Fee", readonly=True)

    def _select(self):
        return super(SaleReport, self)._select() + ", l.mmr_code_p as mmr_code_p" + ", s.mmr_fee as mmr_fee"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", l.mmr_code_p" + ", s.mmr_fee"
