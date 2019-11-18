from datetime import datetime

from odoo import api, fields, models, _

class Quant(models.Model):
    _inherit = "stock.quant"

    def recompute_inventory_value(self):
        for quant in self:
            if quant.company_id != self.env.user.company_id:
                # if the company of the quant is different than the current user company, force the company in the context
                # then re-do a browse to read the property fields for the good company.
                quant = quant.with_context(force_company=quant.company_id.id)
            quant.inventory_value = quant.product_id.standard_price * quant.qty

    def change_inventory_value(self):
        return {
            'name': _('Manual Stock Quant Change'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.quant.change',
            'view_id': self.env.ref('mmr_inventory_ext.stock_quant_change_form_view').id,
            'target': 'new',
        }

