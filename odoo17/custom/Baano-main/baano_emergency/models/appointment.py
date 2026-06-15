
from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
import pytz


class BaanoAppointment(models.Model):
    _name = 'baano.appointment'
    _description = 'Appointment'

    name = fields.Char(string="Consultation Number",
                       readonly=True, copy=False, default="New")
    patient_id = fields.Many2one(
        'baano.patient', required=True, string='Patient')
    company_id_number = fields.Char(
        string="Company ID",
        related="patient_id.company_id_number",
        store=True,
        readonly=True
    )

    age = fields.Integer(string="Patient's Age",
                         related="patient_id.age", store=True, readonly=True)

    doctor_id = fields.Many2one(
        'res.partner',
        string='Doctor',
        required=False,
        # domain="[('is_doctor', '=', True)]",
    )

    appointment_date = fields.Date(
        string='Consultation Date',
        required=True,
        default=fields.Date.context_today,
    )

    lab_request_id = fields.Many2one(
        'laboratory.lab_request', string='Lab Request', readonly=True)

    prescription_id = fields.Many2one(
        'baano.prescription', string='Prescriptions', readonly=True)

    def action_request_lab(self):
        for record in self:
            # if record.state != 'in_consultation':
            #     raise ValidationError(
            #         "Lab request can only be created during consultation.")
            if record.lab_request_id:
                raise ValidationError(
                    "A lab request already exists for this appointment.")
            lab_request = self.env['laboratory.lab_request'].create({
                'appointment_id': record.id,
                'patient_id': record.patient_id.id,
                'doctor_id': record.doctor_id.id,
                'date': fields.Datetime.now(),
                'state': 'draft'
            })
            record.lab_request_id = lab_request.id

    def action_view_lab_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Lab Request',
            'res_model': 'laboratory.lab_request',
            'view_mode': 'form',
            'res_id': self.lab_request_id.id,
            'target': 'current',
        }

    start_time = fields.Float(string='Start Time', required=True,
                              help="Start time of the consultation in 24h format (e.g. 14.5 = 2:30 PM)")
    end_time = fields.Float(string='End Time', required=True,  default=23.59,
                            help="End time of the consultation in 24h format (e.g. 15.75 = 3:45 PM)")

    @api.model
    def create(self, vals):
        # Automatically set consultation date if not provided
        if not vals.get('appointment_date'):
            vals['appointment_date'] = fields.Date.today()
        return super().create(vals)

    def write(self, vals):
        for record in self:
            new_state = vals.get('state')
            if new_state == 'consultation':
                vals['start_time'] = self._get_float_time_now()
            if new_state == 'done':
                vals['end_time'] = self._get_float_time_now()
        return super().write(vals)

    def _get_float_time_now(self):
        local_dt = datetime.now()
        local_dt = local_dt + timedelta(hours=3)
        # Return float hour (e.g., 14.5 for 2:30 PM)
        return local_dt.hour + (local_dt.minute / 60.0)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    # Clinical assessment fields (stored directly in baano.appointment)
    weight = fields.Float(string="Weight (kg)")
    acs_weight_name = fields.Char(string="Weight Unit Label", default="kg")
    height = fields.Float(string="Height (cm)")
    acs_height_name = fields.Char(string="Height Unit Label", default="cm")
    temp = fields.Float(string="Temperature (°C)")
    acs_temp_name = fields.Char(string="Temperature Unit Label", default="°C")
    hr = fields.Integer(string="Heart Rate (bpm)")
    rr = fields.Integer(string="Respiratory Rate")
    systolic_bp = fields.Integer(string="Systolic BP")
    diastolic_bp = fields.Integer(string="Diastolic BP")
    spo2 = fields.Integer(string="SpO2 (%)")
    acs_spo2_name = fields.Char(string="SpO2 Unit Label", default="%")
    rbs = fields.Float(string="Random Blood Sugar (mg/dL)")
    fbs = fields.Float(string="Fasting Blood Sugar (mg/dL)")
    hbl = fields.Float(string="Hemoglobin (g/dL)")
    acs_rbs_name = fields.Char(string="RBS Unit Label", default="mg/dL")
    acs_hbl_name = fields.Char(string="RBS Unit Label", default="g/dL")
    bmi = fields.Float(string="BMI", compute="_compute_bmi", store=True)
    bmi_state = fields.Selection([
        ('underweight', 'Underweight'),
        ('normal', 'Normal'),
        ('overweight', 'Overweight'),
        ('obese', 'Obese'),
    ], string="BMI Category", compute="_compute_bmi", store=True)
    pain_level = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ], string="Pain Level", default="0")
    pain = fields.Selection([
        ('pain_0', 'Pain Free'),
        ('pain_1', 'Pain is very mild, barely noticeable. Most of the time you don’t think about it.'),
        ('pain_2', 'Minor pain. Annoying and may have occasional stronger twinges.'),
        ('pain_3', 'Pain is noticeable and distracting, however, you can get used to it and adapt.'),
        ('pain_4', 'Moderate pain. If you are deeply involved in an activity, it can be ignored for a period of time, but is still distracting.'),
        ('pain_5', 'Moderately strong pain. It can’t be ignored for more than a few minutes, but with effort you still can manage to work or participate in some social activities.'),
        ('pain_6', 'Moderately strong pain that interferes with normal daily activities. Difficulty concentrating.'),
        ('pain_7', 'Severe pain that dominates your senses and significantly limits your ability to perform normal daily activities or maintain social relationships. Interferes with sleep.'),
        ('pain_8', 'Intense pain. Physical activity is severely limited. Conversing requires great effort.'),
        ('pain_9', 'Excruciating pain. Unable to converse. Crying out and/or moaning uncontrollably.'),
        ('pain_10', 'Unspeakable pain. Bedridden and possibly delirious. Very few people will ever experience this level of pain.'),
    ], string="Pain", compute="_get_pain_info", store=True)
    lab_report = fields.Text(string="Laboratory Report")

    # Other medical fields
    medical_complain = fields.Text(string='Medical Complaint')
    vital_signs = fields.Text(string='Vital Signs')
    physical_exam = fields.Text(string='Physical Examination')
    past_medical_history = fields.Text(string='Past Medical History')
    diagnosis_id = fields.Many2one('baano.diseases', string='Diagnosis')
    treatment = fields.Text(string='Treatment')
    notes = fields.Text(string='Notes')

    previous_appointments_ids = fields.Many2many(
        'baano.appointment', string="Previous Appointments", compute="_compute_previous_appointments"
    )

    def _compute_previous_appointments(self):
        for record in self:
            domain = [
                ('patient_id', '=', record.patient_id.id),
                ('appointment_date', '<', record.appointment_date),
            ]
            # Only add ('id', '!=', record.id) if the record is saved (has a real ID)
            if record.id and not isinstance(record.id, models.NewId):
                domain.append(('id', '!=', record.id))
            record.previous_appointments_ids = self.env['baano.appointment'].search(
                domain)

    def action_confirm(self):
        self.write({'state': 'consultation'})

    def action_done(self):
        for rec in self:
            # Create an evaluation snapshot
            self.env['baano.evaluation'].create({
                'appointment_id': rec.id,
                'patient_id': rec.patient_id.id,
                'physician_id': rec.doctor_id.id,
                'weight': rec.weight,
                'height': rec.height,
                'temp': rec.temp,
                'hr': rec.hr,
                'rr': rec.rr,
                'systolic_bp': rec.systolic_bp,
                'diastolic_bp': rec.diastolic_bp,
                'spo2': rec.spo2,
                'rbs': rec.rbs,
                'bmi': rec.bmi,
                'bmi_state': rec.bmi_state,
                'pain_level': rec.pain_level,
                'pain': rec.pain,
                'lab_report': rec.lab_report,
            })
    
            rec.state = 'done'   # or your real state field name
    
        return True




    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('height', 'weight')
    def _compute_bmi(self):
        for rec in self:
            bmi = 0
            bmi_state = False
            if rec.height and rec.weight:
                try:
                    bmi = rec.weight / ((rec.height / 100) ** 2)
                except:
                    bmi = 0

                bmi_state = 'normal'
                if bmi < 18.5:
                    bmi_state = 'underweight'
                elif 25 <= bmi < 30:
                    bmi_state = 'overweight'
                elif bmi >= 30:
                    bmi_state = 'obese'
            rec.bmi = bmi
            rec.bmi_state = bmi_state

    @api.depends('pain_level')
    def _get_pain_info(self):
        """Compute the descriptive pain label based on pain_level."""
        # Mapping numeric level to pain description keys
        level_to_pain = {
            '0': 'pain_0',
            '1': 'pain_1',
            '2': 'pain_2',
            '3': 'pain_3',
            '4': 'pain_4',
            '5': 'pain_5',
            '6': 'pain_6',
            '7': 'pain_7',
            '8': 'pain_8',
            '9': 'pain_9',
            '10': 'pain_10',
        }

        for record in self:
            record.pain = level_to_pain.get(record.pain_level, False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'baano.appointment') or 'New'
        return super(BaanoAppointment, self).create(vals_list)

    def action_prescribe(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'baano.prescription',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_prescribing_doctor': self.doctor_id.id,
                'default_disease_id': self.diagnosis_id.id,
                'default_appointment_id': self.id,
                'default_treatment': self.treatment.id if self.treatment else False,
            },
        }

    def view_prescriptions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescriptions',
            'res_model': 'baano.prescription',
            'view_mode': 'tree,form',
            'target': 'current',
            # Optional: filter by related appointment
            'domain': [('appointment_id', '=', self.id)],
        }
