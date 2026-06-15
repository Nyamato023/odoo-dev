from odoo import fields, models, api, _


class LabResult(models.Model):
    _name = 'laboratory.lab_result'
    _description = 'Lab Result'

    name = fields.Char(string='Result Reference', required=True,
                       copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'laboratory.lab_result') or _('New')
        return super().create(vals)

    request_id = fields.Many2one(
        'laboratory.lab_request', string='Lab Request', required=True)
    patient_id = fields.Many2one(
        'res.partner', string='Patient', required=True)
    date = fields.Datetime(
        string='Date', default=fields.Datetime.now, required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed')
    ], string='Status', default='pending', required=True)
