    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def unlink(self):
        for picking in self:
            self.env['deleted.record.history'].create({'model_id': "Delivery Order", 'record_id': picking.id, 'name': picking.name or 'False'})
        return super(Picking, self).unlink()
