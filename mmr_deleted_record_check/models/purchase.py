# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def unlink(self):
        for purchase in self:
            self.env['deleted.record.history'].create({'model_id': "Purchase Order", 'record_id': purchase.id, 'name': purchase.name or 'False'})
        return super(PurchaseOrder, self).unlink()
