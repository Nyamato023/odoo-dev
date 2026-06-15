from odoo import fields, models, api, _
from odoo.exceptions import UserError


class LabSample(models.Model):
    _name = 'laboratory.lab_sample'
    _description = 'Lab Sample'

    name = fields.Char(string='Sample Reference', required=True,
                       copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'laboratory.lab_sample') or _('New')
        return super().create(vals)

    request_id = fields.Many2one(
        'laboratory.lab_request', string='Lab Request', required=True)
    patient_id = fields.Many2one(
        'res.partner', string='Patient', required=True)
    date = fields.Datetime(
        string='Date', default=fields.Datetime.now, required=True)
    status = fields.Selection([
        ('collected', 'Collected'),
        ('processed', 'Processed')
    ], string='Status', default='collected', required=True)

    def action_process(self):
        if self.status != 'received':
            raise UserError("Sample must be in 'Received' state to process.")
        self.status = 'processed'
