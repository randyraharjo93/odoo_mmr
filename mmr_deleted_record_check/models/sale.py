# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def unlink(self):
        for sale in self:
            self.env['deleted.record.history'].create({'model_id': "Sale Order", 'record_id': sale.id, 'name': sale.name or 'False'})
        return super(SaleOrder, self).unlink()
