from odoo import fields, models, api, _


class LabTest(models.Model):
    _name = 'laboratory.lab_test'
    _description = 'Lab Test'

    name = fields.Char(string='Test Reference', required=True,
                       copy=False, readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'laboratory.lab_test') or _('New')
        return super().create(vals)

    sample_type = fields.Selection([
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('stool', 'Stool'),
        ('swab', 'Swab')
    ], string='Sample Type', required=True)
    result_type = fields.Selection([
        ('numeric', 'Numeric'),
        ('text', 'Text')
    ], string='Result Type', required=True)
    diagnosis = fields.Char(string='Diagnosis')
    normal_range = fields.Char(string='Normal Range')
    result_value = fields.Char(string='Result Value')
    description = fields.Text(string='Description')
    other_info = fields.Text(string='Other Information')
    request_id = fields.Many2one(
        'laboratory.lab_request', string='Lab Request')

    category = fields.Selection([
        ('blood_tests', 'Blood Tests'),
        ('organ_function', 'Organ Function Tests'),
        ('urine_tests', 'Urine Tests'),
        ('infection_tests', 'Infection Screening'),
        ('hormone_tests', 'Hormone Tests'),
        ('immune_tests', 'Immune System Tests'),
        ('stool_tests', 'Stool Tests'),
        ('drug_tests', 'Drug and Toxin Tests'),
        ('virus_tests', 'Viral Tests'),
        ('general_health', 'General Health Checks')
    ], string='Category')
