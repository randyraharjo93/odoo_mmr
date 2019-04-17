# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def action_invoice_open(self):
        result = super(AccountInvoice, self).action_invoice_open()
        # MMR Special Split based on sequence suffix
        #How to do this
        # Prefix "F"
        # Suffix "|%(month)s/%(year)s   "
        if len(self.number.split('|')) > 1:
            name_split = self.number.split('|')
            so_id = self.env['sale.order'].search([('name', '=', self.origin)])
            if so_id:
                middle_name = "/" + (self.company_id.partner_id.ref or "") + "/" + (so_id.user_id.partner_id.ref or "") + "/" + (so_id.team_id.name or "") + "/"
                self.number = name_split[0] + middle_name + name_split[1]
            else:
                if self.origin.split("/", 1):
                    last_name = self.origin.split("/", 1)
                    self.number = name_split[0] + last_name
        return result
