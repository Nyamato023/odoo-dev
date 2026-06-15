from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Boolean field to mark whether the user is a doctor
    is_doctor = fields.Boolean(string='Is a Doctor', default=False)
