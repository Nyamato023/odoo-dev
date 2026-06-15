from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_hospital = fields.Boolean(string="Hospital")