# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
import logging
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def _select_nextval(cr, seq_name):
    cr.execute("SELECT nextval('%s')" % seq_name)
    return cr.fetchone()


def _update_nogap(self, number_increment):
    number_next = self.number_next
    self._cr.execute("SELECT number_next FROM %s WHERE id=%s FOR UPDATE NOWAIT" % (self._table, self.id))
    self._cr.execute("UPDATE %s SET number_next=number_next+%s WHERE id=%s " % (self._table, number_increment, self.id))
    self.invalidate_cache(['number_next'], [self.id])
    return number_next


class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    def _next(self):
        if self.sequence_id.implementation == 'standard':
            current_number = self.number_next
            current_number_actual = self.number_next_actual
            number_next = _select_nextval(self._cr, 'ir_sequence_%03d_%03d' % (self.sequence_id.id, self.id))
            self.env['ir.sequence.log'].create({'name': '', 'sequence_id': self.sequence_id.id, 'sequence_date_range_id': self.id, 'message': 'Current Number: ' + str(current_number) + ' Current Number Actual: ' + str(current_number_actual) + ' Next Number: ' + str(number_next)})
        else:
            number_next = _update_nogap(self, self.sequence_id.number_increment)
        return self.sequence_id.get_next_char(number_next)
