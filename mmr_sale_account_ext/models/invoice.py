# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    mmr_internal_code = fields.Char("Internal Code", compute="_get_internal_code_name")
    mmr_multiple_so_code = fields.Char("Multiple So Code")
    mmr_no_so_code = fields.Char("No So Code")

    @api.one
    def _get_internal_code_name(self):
        if any(account_line.sale_line_ids for account_line in self.invoice_line_ids):
            if len(self.invoice_line_ids.mapped('sale_line_ids')) > 1:
                self.mmr_internal_code = self.mmr_multiple_so_code
            else:
                sale_order_id = self.invoice_line_ids.mapped('sale_line_ids')[0].order_id
                if len(sale_order_id.invoice_ids) > 1:
                    so_mmr_internal_code = sale_order_id.mmr_internal_code[2:] if sale_order_id.mmr_internal_code else "-"
                    invoice_ids = sale_order_id.invoice_ids.ids
                    invoice_ids.sort()
                    self.mmr_internal_code = "INV" + so_mmr_internal_code + " " + chr(65 + invoice_ids.index(self.id))
                else:
                    so_mmr_internal_code = sale_order_id.mmr_internal_code[2:] if sale_order_id.mmr_internal_code else "-"
                    self.mmr_internal_code = "INV" + so_mmr_internal_code
        else:
            self.mmr_internal_code = self.mmr_no_so_code

    @api.model
    def create(self, vals):
        result = super(AccountInvoice, self).create(vals)
        if any(account_line.sale_line_ids for account_line in result.invoice_line_ids):
            if len(result.invoice_line_ids.mapped('sale_line_ids')) > 1:
                if result.company_id:
                    result.mmr_multiple_so_code = result.env['ir.sequence'].with_context(force_company=result.company_id.id).next_by_code('mmr.account.multiple.so.sequence') or _('New')
                else:
                    result.mmr_multiple_so_code = result.env['ir.sequence'].next_by_code('mmr.account.multiple.so.sequence') or _('New')
        else:
            if result.company_id:
                result.mmr_no_so_code = self.env['ir.sequence'].with_context(force_company=result.company_id.id).next_by_code('mmr.account.no.so.sequence') or _('New')
            else:
                result.mmr_no_so_code = self.env['ir.sequence'].next_by_code('mmr.account.no.so.sequence') or _('New')
        return result
