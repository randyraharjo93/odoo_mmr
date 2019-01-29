# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
import logging

_logger = logging.getLogger(__name__)


class MMRVisit(models.Model):
    _name = "mmr.visit"
    _rec_name = 'partner_id'
    _inherit = ['mail.thread']

    # General Info
    partner_id = fields.Many2one("res.partner", "Customer", required=True, track_visibility='onchange')
    product_ids = fields.Many2many("product.product", string="Product", domain=[('sale_ok', '=', True)])
    state = fields.Selection([('plan', "Planned"),
                              ('visit', 'Visited'),
                              ('report', "Reported"),
                              ('cancel', "Cancelled")],
                              default="plan", track_visibility='onchange')
    salesperson_user_id = fields.Many2one("res.users", "Salesperson", required=True, track_visibility='onchange')
    sale_team_id = fields.Many2one("crm.team", "Rayon")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    tag_ids = fields.Many2many("mmr.visit.tag", string="Tags")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id, help="Company related to this visit")
    # Plan
    planned_date = fields.Datetime("Planned Date", required=True, track_visibility='onchange')
    plan_note = fields.Text("Plan Description")
    # Result
    result_description = fields.Text("Result Description")
    visit_date = fields.Datetime("Visit Date", track_visibility='onchange')
    visit_result_id = fields.Many2one('mmr.visit.result', "Visit Result", track_visibility='onchange')
    # Cancel
    cancel_reason_id = fields.Many2one('mmr.visit.cancel', 'Cancel Reason', track_visibility='onchange')

    @api.multi
    def button_cancel_wizard(self):
        return {
            'name': _('Cancel Visit'),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'mmr.visit.management.cancel.wizard',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('mmr_customer_visit_management.mmr_visit_cancel_wizard').id,
        }

    @api.multi
    def button_draft(self):
        self.write({'state': 'plan'})

class MMRVisitCancel(models.Model):
    _name = "mmr.visit.cancel"

    name = fields.Char("Name")


class MMRVisitResult(models.Model):
    _name = "mmr.visit.result"

    name = fields.Char("Name")

class MMRVisitTag(models.Model):
    _name = "mmr.visit.tag"

    name = fields.Char("Name")
