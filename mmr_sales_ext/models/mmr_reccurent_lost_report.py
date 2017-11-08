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
        		sale_order_line_id = self.env['sale.order.line'].search([('product_id', '=', product.id), ('order_partner_id', '=', partner.id), ('order_id.confirmation_date', '!=', False)], limit=1)
        		if sale_order_line_id:
        			self.create({'partner_id': sale_order_line_id.order_partner_id.id, 'product_id': sale_order_line_id.product_id.id, 'last_purchase': sale_order_line_id.order_id.confirmation_date, 'last_salesperson_user_id': sale_order_line_id.order_id.user_id and sale_order_line_id.order_id.user_id.id or False, 'last_sale_team_id': sale_order_line_id.order_id.team_id and sale_order_line_id.order_id.team_id.id or False, 'date_since_last_purchase': (fields.datetime.now()-fields.datetime.strptime(sale_order_line_id.order_id.confirmation_date, DTF)).days})
