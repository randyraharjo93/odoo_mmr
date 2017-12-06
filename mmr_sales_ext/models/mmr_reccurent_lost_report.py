# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import logging

_logger = logging.getLogger(__name__)


class MMRRecurrentLostReport(models.Model):
    _name = "mmr.reccurent.lost.report"

    partner_id = fields.Many2one("res.partner", "Customer")
    product_id = fields.Many2one("product.product", "Product")
    last_purchase = fields.Datetime("Last Purchase")
    last_salesperson_user_id = fields.Many2one("res.users", "Last Salesperson")
    last_sale_team_id = fields.Many2one("crm.team", "Last Rayon")
    date_since_last_purchase = fields.Float("# Dates since last purchase")
    active = fields.Boolean("Active", default=True)
    last_price = fields.Float("Last Price")
    last_discount = fields.Float("Discount")

    @api.model
    def _cron_generate_sales_recurrent_lost_report(self):
    	self.search([]).write({'active': False})
    	partner_ids = self.env['res.partner'].search([])
    	partner_count = 1
        for partner in partner_ids:
        	_logger.info('Partner : ' + str(partner_count) + 'of' + str(len(partner_ids)))
        	partner_count += 1
        	product_ids = self.env['product.product'].search([])
        	for product in product_ids:
        		sale_order_line_id = self.env['sale.order.line'].search([('product_id', '=', product.id), ('order_partner_id', '=', partner.id), ('order_confirmation_date', '!=', False), ('state', '=', 'sale')], order="order_confirmation_date desc", limit=1)
        		if sale_order_line_id:
        			self.create({'partner_id': sale_order_line_id.order_partner_id.id, 'last_price': sale_order_line_id.price_unit, 'last_discount': sale_order_line_id.discount, 'product_id': sale_order_line_id.product_id.id, 'last_purchase': sale_order_line_id.order_id.confirmation_date, 'last_salesperson_user_id': sale_order_line_id.order_id.user_id and sale_order_line_id.order_id.user_id.id or False, 'last_sale_team_id': sale_order_line_id.order_id.team_id and sale_order_line_id.order_id.team_id.id or False, 'date_since_last_purchase': (fields.datetime.now()-fields.datetime.strptime(sale_order_line_id.order_id.confirmation_date, DTF)).days})
