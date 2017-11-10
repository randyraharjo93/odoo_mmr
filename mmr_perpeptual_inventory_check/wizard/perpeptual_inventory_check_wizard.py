# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class MMRPerpeptualInventoryCheck(models.TransientModel):
    _name = "mmr.perpeptual.inventory.check"

    stock_in_account_move_line_ids = fields.Many2many("account.move.line", 'stock_in_account_move_line_ids_account_move_line_rel', 'wizard_id', 'account_id')
    invoice_in_account_move_line_ids = fields.Many2many("account.move.line", 'invoice_in_account_move_line_ids_account_move_line_rel', 'wizard_id', 'account_id')
    stock_in_total_value = fields.Float("Total Value")
    invoice_in_total_value = fields.Float("Total Value")

    @api.multi
    def stock_in_check(self):
        account_move_line_ids = [stock_input_account_id.property_stock_account_input_categ_id.id for stock_input_account_id in self.env['product.category'].search([]) if stock_input_account_id.property_stock_account_input_categ_id.id]
        account_move_line_ids = list(set(account_move_line_ids))
        used_account_move_line_ids = []
        reverse_move_line_not_found_ids = []
        total_value = 0
        for account_move_line_id in self.env['account.move.line'].search([('account_id', 'in', account_move_line_ids), ('credit', '>', 0), ('partner_id', '!=', False)]):
            reverse_move_line_id = self.env['account.move.line'].search([('account_id', '=', account_move_line_id.account_id.id), ('debit', '=', account_move_line_id.credit), ('partner_id', '=', account_move_line_id.partner_id.id), ('id', 'not in', used_account_move_line_ids)], limit=1)
            if reverse_move_line_id:
                used_account_move_line_ids.append(reverse_move_line_id.id)
            else:
                reverse_move_line_not_found_ids.append(account_move_line_id.id)
                total_value += account_move_line_id.credit
        self.stock_in_account_move_line_ids = [(6, 0, reverse_move_line_not_found_ids)]
        self.stock_in_total_value = total_value

    @api.multi
    def invoice_in_check(self):
        account_move_line_ids = [stock_input_account_id.property_stock_account_input_categ_id.id for stock_input_account_id in self.env['product.category'].search([]) if stock_input_account_id.property_stock_account_input_categ_id.id]
        account_move_line_ids = list(set(account_move_line_ids))
        used_account_move_line_ids = []
        reverse_move_line_not_found_ids = []
        total_value = 0
        for account_move_line_id in self.env['account.move.line'].search([('account_id', 'in', account_move_line_ids), ('debit', '>', 0), ('partner_id', '!=', False)]):
            reverse_move_line_id = self.env['account.move.line'].search([('account_id', '=', account_move_line_id.account_id.id), ('credit', '=', account_move_line_id.credit), ('partner_id', '=', account_move_line_id.partner_id.id), ('id', 'not in', used_account_move_line_ids)], limit=1)
            if reverse_move_line_id:
                used_account_move_line_ids.append(reverse_move_line_id.id)
            else:
                reverse_move_line_not_found_ids.append(account_move_line_id.id)
                total_value += account_move_line_id.credit
        self.invoice_in_account_move_line_ids = [(6, 0, reverse_move_line_not_found_ids)]
        self.invoice_in_total_value = total_value

    @api.multi
    def do_inventory_check(self):
        self.stock_in_check()
        self.invoice_in_check()
        return self.env['report'].get_action(self, 'mmr_perpeptual_inventory_check.report_mmr_perpeptual_check')
