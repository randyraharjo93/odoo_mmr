# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' ('+po.partner_ref+')'
            # Don't show Price for normal purchase user
            if po.amount_total and self.user_has_groups("purchase.group_purchase_manager"):
                name += ': ' + formatLang(self.env, po.amount_total, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result

    filtered_message_ids = fields.Many2many("mail.message", compute="_get_save_message_ids")

    @api.one
    @api.depends('message_ids')
    def _get_save_message_ids(self):
        if self.message_ids:
            message_ids = []
            for message_id in self.message_ids:
                if not message_id.tracking_value_ids:
                    message_ids.append(message_id.id)
            self.filtered_message_ids = [(6, 0, message_ids)]
