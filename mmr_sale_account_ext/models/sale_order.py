# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('invoice_lines.invoice_id.state')
    def _compute_payment_status(self):
        for line in self:
            if all(invoice.invoice_id.state == 'paid' for invoice in line.invoice_lines):
                # There is a payment already
                line.payment_status = 'paid'
            elif any(invoice.invoice_id.state == 'open' for invoice in line.invoice_lines):
                # But if there is an open invoice
                line.payment_status = 'open'
            else:
                # Always start with No
                line.payment_status = 'no'

    payment_status = fields.Selection([
        ('no', 'No Invoice'),
        ('open', 'Open'),
        ('paid', 'Paid')
        ], string='Payment Status', compute='_compute_payment_status', store=True, readonly=True, default='no')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('state', 'order_line.payment_status')
    def _get_paid(self):
        for order in self:
            if order.state not in ('sale', 'done'):
                order.payment_status = 'no'
            elif any(order_line.payment_status == 'open' for order_line in order.order_line):
                order.payment_status = 'open'
            elif all(order_line.payment_status == 'paid' for order_line in order.order_line):
                order.payment_status = 'paid'
            else:
                order.payment_status = 'no'

    payment_status = fields.Selection([
        ('no', 'No Invoice'),
        ('open', 'Open'),
        ('paid', 'Paid')
        ], string='Payment Status', compute='_get_paid', store=True, readonly=True, default='no')


