# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

import odoo.addons.decimal_precision as dp


class SuppliferInfo(models.Model):
    _inherit = "product.supplierinfo"

    delay = fields.Integer(
        'Delivery Lead Time', default=7)
