from odoo import models, fields

class BaanoSite(models.Model):
    _name = 'baano.site'
    _description = 'Site'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
