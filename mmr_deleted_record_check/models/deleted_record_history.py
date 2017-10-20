# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class DeletedRecordHistory(models.Model):
    _name = "deleted.record.history"

    name = fields.Char("Name")
    model_id = fields.Char("Model")
    record_id = fields.Integer("Record ID")
