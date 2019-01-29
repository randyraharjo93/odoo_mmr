# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class VisitManagementCancel(models.TransientModel):
    _name = 'mmr.visit.management.cancel.wizard'

    cancel_reason_id = fields.Many2one('mmr.visit.cancel', 'Cancel Reason', required=True)

    def do_cancel(self):
        if self._context.get('active_id'):
            active_visit = self.env['mmr.visit'].browse(self._context.get('active_id'))
            active_visit.write({'cancel_reason_id': self.cancel_reason_id.id, 'state': 'cancel'})
