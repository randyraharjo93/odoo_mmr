# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Picking(models.Model):
    _inherit = "stock.picking"

    mmr_internal_code = fields.Char("Internal Code", compute="_get_internal_code_name")

    @api.one
    def _get_internal_code_name(self):
        if self.sale_id:
            if len(self.sale_id.picking_ids) > 1:
                so_mmr_internal_code = self.sale_id.mmr_internal_code[2:] if self.sale_id.mmr_internal_code else "-"
                picking_ids = self.sale_id.picking_ids.ids
                picking_ids.sort()
                self.mmr_internal_code = "DO" + so_mmr_internal_code + " " + chr(65 + picking_ids.index(self.id))
            else:
                so_mmr_internal_code = self.sale_id.mmr_internal_code[2:] if self.sale_id.mmr_internal_code else "-"
                self.mmr_internal_code = "DO" + so_mmr_internal_code
        else:
            if self.company_id:
                self.mmr_internal_code = self.env['ir.sequence'].with_context(force_company=self.company_id.id).next_by_code('mmr.inventory.no.so.sequence') or _('New')
            else:
                self.mmr_internal_code = self.env['ir.sequence'].next_by_code('mmr.inventory.no.so.sequence') or _('New')
