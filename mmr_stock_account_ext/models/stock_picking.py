# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Picking(models.Model):
    _inherit = "stock.picking"

    mmr_account_move_ids = fields.Many2many("account.move", string="Journal Entries", compute="_get_journal_entry")

    @api.one
    def _get_journal_entry(self):
        self.mmr_account_move_ids = [(6, 0, self.env['account.move'].search(['|', ('ref', 'ilike', self.name), ('name', 'ilike', self.name)]).ids)]
