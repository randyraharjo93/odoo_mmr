# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def unlink(self):
        for invoice in self:
            self.env['deleted.record.history'].create({'model_id': "Account Invoice", 'record_id': invoice.id, 'name': invoice.name or 'False'})
        return super(AccountInvoice, self).unlink()
