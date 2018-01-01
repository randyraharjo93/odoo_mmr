# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import logging

_logger = logging.getLogger(__name__)


class MMRVisit(models.Model):
    _name = "mmr.visit"
    _rec_name = 'partner_id'

    partner_id = fields.Many2one("res.partner", "Customer", required=True)
    product_ids = fields.Many2many("product.product", string="Product")
    planned_date = fields.Datetime("Planned Date", required=True)
    plan_note = fields.Text("Plan Description")
    result_description = fields.Text("Result Description")
    visit_date = fields.Datetime("Visit Date")
    state = fields.Selection([('plan', "Planned"),
                              ('visit', 'Visited'),
                              ('report', "Reported"),
                              ('cancel', "Cancelled")],
                              default="plan")
    cancel_reason_id = fields.Many2one('mmr.visit.cancel', 'Cancel Reason')
    visit_result_id = fields.Many2one('mmr.visit.result', "Visit Result")
    salesperson_user_id = fields.Many2one("res.users", "Salesperson", required=True)
    sale_team_id = fields.Many2one("crm.team", "Rayon")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    tag_ids = fields.Many2many("mmr.visit.tag", string="Tags")


class MMRVisitCancel(models.Model):
    _name = "mmr.visit.cancel"

    name = fields.Char("Name")


class MMRVisitResult(models.Model):
    _name = "mmr.visit.result"

    name = fields.Char("Name")

class MMRVisitTag(models.Model):
    _name = "mmr.visit.tag"

    name = fields.Char("Name")
