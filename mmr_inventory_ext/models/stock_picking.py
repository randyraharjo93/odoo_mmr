# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        result = super(Picking, self).create(vals)
        # MMR Special Split based on sequence suffix
        if result.name.split('|'):
            name_split = result.name.split('|')
            so_id = self.env['sale.order'].search([('name', '=', result.origin)])
            if so_id:
                middle_name = "/" + (result.company_id.partner_id.ref or "") + "/" + (so_id.user_id.partner_id.ref or "") + "/" + (so_id.team_id.name or "") + "/"
                result.name = name_split[0] + middle_name + name_split[1]
            else:
                if result.origin.split("/", 1):
                    last_name = result.origin.split("/", 1)
                    result.name = name_split[0] + last_name
        return result
