from odoo import models, fields

class BaanoSite(models.Model):
    _name = 'baano.site'
    _description = 'Patient Site'

    name = fields.Char(required=True)
    code = fields.Char()
    company_id = fields.Many2one('res.company', string="Company", required=True)
