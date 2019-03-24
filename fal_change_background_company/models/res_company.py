from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    background_image = fields.Binary(string="Background Image", attachment=True)
    background_image_fname = fields.Char(string="Background Image Name")
    navbar_image = fields.Binary(string="Nav Bar Image", attachment=True)
    navbar_image_fname = fields.Char(string="Nav Bar Image Name")
