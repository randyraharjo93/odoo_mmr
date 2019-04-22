# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    filtered_message_ids = fields.Many2many("mail.message", compute="_get_save_message_ids")

    @api.one
    @api.depends('message_ids')
    def _get_save_message_ids(self):
        if self.message_ids:
            message_ids = []
            for message_id in self.message_ids:
                if not message_id.sudo().tracking_value_ids:
                    message_ids.append(message_id.id)
            self.sudo().filtered_message_ids = [(6, 0, message_ids)]
