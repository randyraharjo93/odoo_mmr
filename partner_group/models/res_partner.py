# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_group_ids = fields.Many2many("res.partner.group", "partner_partnergroup_rel", "partner_id", "group_id", string="Groups")
