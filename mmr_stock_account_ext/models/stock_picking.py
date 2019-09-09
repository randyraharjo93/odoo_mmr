# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Picking(models.Model):
    _inherit = "stock.picking"

    mmr_account_move_ids = fields.Many2many("account.move", string="Journal Entries", compute="_get_journal_entry")
    mmr_invoice_date = fields.Date('Invoice Date', compute="_get_invoice_date")

    @api.one
    def _get_journal_entry(self):
        if self.user_has_groups('account.group_account_user'):
            self.mmr_account_move_ids = [(6, 0, self.env['account.move'].search(['|', ('ref', 'ilike', self.name), ('name', 'ilike', self.name)]).ids)]

    @api.one
    def _get_invoice_date(self):
        if self.user_has_groups('account.group_account_user'):
            if self.sale_id:
                for invoice_id in self.sale_id.invoice_ids:
                    self.mmr_invoice_date = invoice_id.date_invoice
            elif self.purchase_id:
                for invoice_id in self.purchase_id.invoice_ids:
                    self.mmr_invoice_date = invoice_id.date_invoice
            else:
                self.mmr_invoice_date = False
