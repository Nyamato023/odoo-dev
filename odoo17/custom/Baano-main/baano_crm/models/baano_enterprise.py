from odoo import models, fields

class BaanoEnterprise(models.Model):
    _name = 'baano.enterprise'
    _description = 'Enterprise'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    site_id = fields.Many2one('baano.site', string='Site', tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
