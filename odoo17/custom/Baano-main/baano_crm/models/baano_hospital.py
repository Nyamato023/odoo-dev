from odoo import models, fields

class BaanoHospital(models.Model):
    _name = 'baano.hospital'
    _description = 'Hospital'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)

