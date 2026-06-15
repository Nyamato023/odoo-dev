from odoo import models, fields

class BaanoDoctor(models.Model):
    _name = 'baano.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
