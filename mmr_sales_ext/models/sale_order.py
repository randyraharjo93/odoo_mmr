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

    # Adding some required field

    mmr_code_p = fields.Boolean(string='Code P', track_visibility='onchange')

    # Onchange Code P
    @api.onchange('order_partner_id', 'product_id')
    def _onchange_code_p(self):
        if self.order_partner_id and self.product_id:
            if self.env['code.p.list'].search([('partner_id', '=', self.order_partner_id.id), ('product_id', '=', self.product_id.id)]):
                self.mmr_code_p = True
            else:
                self.mmr_code_p = False


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if not self.user_has_groups('base.group_erp_manager'):
                for order_line in order.order_line:
                    unit_price_final = order_line.price_subtotal / order_line.product_uom_qty
                    if unit_price_final < order_line.product_id.lst_price:
                        raise UserError(_("Price of Product :" + order_line.product_id.display_name + " is lower than the minimum sale price. Please contact manager to confirm the sale."))
        return res
