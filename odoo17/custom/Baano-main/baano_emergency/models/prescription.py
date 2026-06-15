from odoo import models, fields, api


class Prescription(models.Model):
    _name = 'baano.prescription'
    _description = 'Prescription'

    name = fields.Char(string="Prescription",
                       readonly=True, copy=False, default="New")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'baano.prescription') or 'New'
        return super(Prescription, self).create(vals_list)

    patient_id = fields.Many2one(
        'baano.patient',
        string='Patient',
        required=True,
        ondelete='restrict'
    )
    prescribing_doctor = fields.Many2one('res.partner',
                                         required=True,
                                         # domain="[('is_doctor', '=', True)]",
                                         string='Prescribing Doctor')

    medicaments_group = fields.Char(string='Medicaments Group')

    disease_id = fields.Many2one(
        'baano.diseases',
        string='Diseases',
        ondelete='restrict'
    )

    prescription_date = fields.Datetime(
        string='Prescription Date', default=fields.Datetime.now)
    pregnancy_warning = fields.Boolean(string='Pregnancy Warning')

    kit = fields.Boolean(string='Kit')
    old_prescription = fields.Boolean(string='Old Prescription')

    appointment_id = fields.Many2one(
        'baano.appointment',
        string='Appointment',
        ondelete='restrict'
    )

    treatment = fields.Char(string='Treatment')
    pickings = fields.Boolean(string='Pickings')

    prescription_lines = fields.One2many(
        'baano.prescription.line', 'prescription_id', string='Prescription Lines')


class PrescriptionLine(models.Model):
    _name = 'baano.prescription.line'
    _description = 'Prescription Line'

    prescription_id = fields.Many2one(
        'baano.prescription', string='Prescription')
    medicine_id = fields.Many2one(
        'baano.medicine',
        string='Medicine',
        required=True,
        ondelete='restrict'
    )
    product_type = fields.Char(string='Product Type')
    name = fields.Char(string='Name')
    dosage_frequency = fields.Char(string='Dosage/Frequency')
    qty_dose = fields.Integer(string='Qty Dose')
    days = fields.Integer(string='Days')
    total_qty = fields.Integer(string='Total Qty')
    comment = fields.Char(string='Comment')
