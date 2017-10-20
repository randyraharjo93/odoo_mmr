# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    mmr_UOM = fields.Char("UoM", help="MCM have unique Unit of Measure that serve just as description.")
