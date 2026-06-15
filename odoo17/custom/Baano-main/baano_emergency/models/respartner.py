from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_doctor = fields.Boolean(string='Is a Doctor', default=False)
