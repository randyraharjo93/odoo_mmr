# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class CodePList(models.Model):
    _name = 'code.p.list'

    # Adding some required field

    partner_id = fields.Many2one("res.partner", "Customer", domain=[('customer', '=', True)])
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)])


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.depends('invoice_lines.invoice_id.state')
    def _compute_payment_status(self):
        for line in self:
            if any(invoice.invoice_id.state == 'paid' for invoice in line.invoice_lines):
                # There is a payment already
                line.payment_status = 'paid'
            elif any(invoice.invoice_id.state == 'open' for invoice in line.invoice_lines):
                # But if there is an open invoice
                line.payment_status = 'open'
            else:
                # Always start with No
                line.payment_status = 'no'

    # Adding some required field
    payment_status = fields.Selection([
        ('no', 'No Invoice'),
        ('open', 'Open'),
        ('paid', 'Paid')
        ], string='Payment Status', compute='_compute_payment_status', store=True, readonly=True, default='no')
    mmr_code_p = fields.Boolean(string='Code P', track_visibility='onchange')
    mmr_mou_id = fields.Many2one("mmr.mou", "MoU")
    order_confirmation_date = fields.Datetime("Confirm Date", related="order_id.confirmation_date", store=True)
    mmr_internal_code = fields.Char("Internal Code", related="order_id.mmr_internal_code", store=True)

    # Onchange Code P
    @api.onchange('order_partner_id', 'product_id')
    def _onchange_code_p(self):
        if self.order_partner_id and self.product_id:
            if self.env['code.p.list'].search([('partner_id', '=', self.order_partner_id.id), ('product_id', '=', self.product_id.id)]):
                self.mmr_code_p = True
            else:
                self.mmr_code_p = False

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        vals = {}
        vals['name'] = '/'
        self.update(vals)
        return result

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Add Current Delivery Information
        """
        self.ensure_one()

        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        expired_date_description = ""
        for picking in self.order_id.picking_ids.filtered(lambda r: not r.mmr_checked_in_invoice and r.state == 'done'):
            picking.mmr_checked_in_invoice = True
            for operation in picking.pack_operation_product_ids.filtered(lambda r:r.product_id == self.product_id):
                for lot in operation.pack_lot_ids:
                    expired_date_description += "[" + lot.lot_id.name + "] : " + str(lot.qty) + " "
        res['name'] = expired_date_description or "/"
        return res


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
    mmr_fee = fields.Monetary("Fee", track_visibility='onchange')
    mmr_internal_code = fields.Char("Internal Code")
    mmr_internal_code_number = fields.Char("Internal Code Number")

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if not self.user_has_groups('sales_team.group_sale_manager'):
                for order_line in order.order_line:
                    unit_price_final = order_line.price_subtotal / order_line.product_uom_qty
                    if unit_price_final < order_line.product_id.lst_price:
                        raise UserError(_("Price of Product :" + order_line.product_id.display_name + " is lower than the minimum sale price. Please contact manager to confirm the sale."))
        return res

    @api.multi
    def action_name_refresh(self):
        if self.mmr_internal_code_number:
            code_number = self.mmr_internal_code_number
        else:
            code_number = "-"
        if self.company_id:
            company_ref = self.env['res.company'].browse(self.company_id.id).partner_id.ref or "-"
        else:
            code_number = "-"
        if self.user_id:
            salesperson_ref = self.env['res.users'].browse(self.user_id.id).partner_id.ref or "-"
        else:
            salesperson_ref = "-"
        if self.team_id:
            team_ref = self.env['crm.team'].browse(self.team_id.id).name or "-"
        else:
            team_ref = "-"
        if self.date_order:
            date_format = self.date_order[5:7] + "/" + self.date_order[0:4]
        else:
            date_format = "-"
        self.mmr_internal_code = code_number + "/" + company_ref + "/" + salesperson_ref + "/" + team_ref + "/" + date_format

    @api.model
    def create(self, vals):
        # Construct MMR Internal Code
        if 'company_id' in vals:
            code_number = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('mmr.sale.sequence') or _('New')
            vals['mmr_internal_code_number'] = code_number
            company_ref = self.env['res.company'].browse(vals['company_id']).partner_id.ref or "-"
        else:
            code_number = self.env['ir.sequence'].next_by_code('mmr.sale.sequence') or _('New')
            vals['mmr_internal_code_number'] = code_number
            company_ref = "-"
        if 'user_id' in vals:
            salesperson_ref = self.env['res.users'].browse(vals['user_id']).partner_id.ref or "-"
        else:
            salesperson_ref = "-"
        if 'team_id' in vals:
            team_ref = self.env['crm.team'].browse(vals['team_id']).name or "-"
        else:
            team_ref = "-"
        if 'date_order' in vals:
            date_format = vals['date_order'][5:7] + "/" + vals['date_order'][0:4]
        else:
            date_format = "-"
        vals['mmr_internal_code'] = code_number + "/" + company_ref + "/" + salesperson_ref + "/" + team_ref + "/" + date_format

        result = super(SaleOrder, self).create(vals)
        return result
