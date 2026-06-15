from odoo import models, fields, api

class BaanoTarget(models.Model):
    _name = 'baano.target'
    _description = 'Baano Targets'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'service_type'
    _order = 'date_start desc, sequence asc, id asc'

    active = fields.Boolean(default=True, tracking=True)
    date = fields.Date(string='Date', tracking=True)
    date_start = fields.Datetime(string='Start Date', tracking=True)
    date_stop = fields.Datetime(string='End Date', tracking=True)
    sequence = fields.Integer(default=10)
    
    # Matching product of type services
    service_type = fields.Selection([
        ('online', 'Online Consultation'),
        ('hospital', 'Hospital Booking'),
        ('enterprise', 'Enterprise'),
        ('home', 'Home Care')
    ], string='Services', help="Target Service", tracking=True, required=True)
    target_count = fields.Integer(string='Target Count', tracking=True)
    
    line_ids = fields.One2many('baano.target.line', 'target_id', string='Target Lines')

class BaanoTargetLine(models.Model):
    _name = 'baano.target.line'
    _description = 'Baano Target Line'
    _order = 'sequence asc, id asc'

    target_id = fields.Many2one('baano.target', string='Parent Target', ondelete='cascade')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    sequence = fields.Integer(default=10)
    
    # Matching product of type services
    service_type = fields.Selection([
        ('online', 'Online Consultation'),
        ('hospital', 'Hospital Booking'),
        ('enterprise', 'Enterprise'),
        ('home', 'Home Care')
    ], string='Services')
    target_count = fields.Integer(string='Target Count')
