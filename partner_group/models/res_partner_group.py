# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartnerGroup(models.Model):
    _name = "res.partner.group"

    name = fields.Char("Name")
    partner_ids = fields.Many2many("res.partner", "partner_partnergroup_rel", "group_id", "partner_id", string="Partners")
    color = fields.Char("Color")
