from odoo import models, fields

class BaanoLocationState(models.Model):
    _name = 'baano.location_state'
    _description = 'Locations / State'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Location', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
