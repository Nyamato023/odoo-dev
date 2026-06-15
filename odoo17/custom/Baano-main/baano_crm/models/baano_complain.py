from odoo import models, fields

class BaanoComplain(models.Model):
    _name = 'baano.complain'
    _description = 'Complain'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Chief Complaint', required=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
