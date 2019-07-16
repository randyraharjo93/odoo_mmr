# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class HrExpense(models.Model):
    _inherit = "hr.expense"

    employee_id = fields.Many2one(string="Submiter")
    employee_who_do_the_expense_id = fields.Many2one('hr.employee', string='Employee')
