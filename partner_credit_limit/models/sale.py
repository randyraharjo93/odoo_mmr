# -*- coding: utf-8 -*-
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def check_limit(self):
        """Check if credit limit for partner was exceeded."""
        self.ensure_one()
        partners = []
        partner = self.partner_id
        partner_parent_id = self.partner_id.parent_id
        partners.append(partner.id)
        if partner_parent_id:
            partners.append(partner_parent_id.id)
            partner = partner_parent_id

        moveline_obj = self.env['account.move.line']
        movelines = moveline_obj.\
            sudo().search([('partner_id', 'in', partners),
                    ('account_id.user_type_id.type', 'in', ['receivable', 'payable']), ('move_id.state', '=', 'posted')])
        confirm_sale_order = self.search([('partner_id', 'in', partners),
                                          ('state', '=', 'sale')])
        debit, credit = 0.0, 0.0
        amount_total = 0.0
        for status in confirm_sale_order:
            amount_total += status.amount_total
        for line in movelines:
            credit += line.credit
            debit += line.debit
        partner_credit_limit = (partner.credit_limit - debit) + credit
        available_credit_limit = ((partner_credit_limit -
                                   (amount_total - debit)) + self.amount_total)

        # Checking on 2 sides
        # A: From the Sales Order PoV, with risk of Invoice without sales order
        # B: From Invoice point of View, with risk of confirming Sales Order if there is a lot of Confirmed SO
        # if ((amount_total + self.amount_total - debit) > partner_credit_limit) or (partner_credit_limit - self.amount_total < 0):
        #     # Consider partners who are under a company.
        #     if not partner.over_credit:
        #         msg = 'Your available credit limit'\
        #               ' Amount = %s \nCheck "%s" Accounts or Credit ' \
        #               'Limits.' % (available_credit_limit,
        #                            self.partner_id.name)
        #         raise UserError(_('You can not confirm Sale Order. \n' + msg))
        #     partner.write({'credit_limit': debit + self.amount_total})
        return True

    @api.multi
    def action_confirm(self):
        """Extend to check credit limit before confirming sale order."""
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.check_limit()
        return res
