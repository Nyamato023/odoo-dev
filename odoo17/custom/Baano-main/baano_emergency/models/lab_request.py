from odoo import fields, models, api, _


class LabRequest(models.Model):
    _name = 'laboratory.lab_request'
    _description = 'Lab Request'

    name = fields.Char(string='Request Reference', required=True,
                       copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'laboratory.lab_request') or _('New')
        return super().create(vals)

    appointment_id = fields.Many2one(
        'baano.appointment', string='Appointment', required=True)

    patient_id = fields.Many2one(
        'res.partner', string='Patient', required=True)
    age = fields.Integer(string='Age')
    date = fields.Datetime(
        string='Date', default=fields.Datetime.now, required=True)
    doctor_id = fields.Many2one(
        'res.partner', string='Prescribing Doctor', required=True)
    test_ids = fields.Many2many(
        'laboratory.lab_test', 'lab_request_test_rel',
        'request_id', 'test_id', string='Tests')

    sample_ids = fields.One2many(
        'laboratory.lab_sample', 'request_id', string='Samples')
    other_info = fields.Text(string='Other Information')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Status', default='draft', required=True)

    def action_confirm(self):
        self.state = 'in_progress'

    def action_done(self):
        for record in self:
            if not all(sample.status == 'processed' for sample in record.sample_ids):
                raise ValidationError(
                    "Cannot mark as Done: All samples must be in 'Processed' state.")
            record.state = 'done'
