from odoo import models, fields


class BaanoEvaluation(models.Model):
    _name = 'baano.evaluation'
    _description = 'Clinical Evaluation'

    appointment_id = fields.Many2one(
        'baano.appointment', string="Appointment", required=True, ondelete='cascade')
    patient_id = fields.Many2one(
        'baano.patient', string="Patient", required=True, related="appointment_id.patient_id", store=True)
    physician_id = fields.Many2one(
        'res.partner', string="Physician", required=False, related="appointment_id.doctor_id", store=True)

    # Clinical assessment fields (related to appointment_id)
    weight = fields.Float(
        related="appointment_id.weight", string="Weight (kg)", readonly=True)
    acs_weight_name = fields.Char(
        related="appointment_id.acs_weight_name", string="Weight Unit Label", readonly=True)
    height = fields.Float(
        related="appointment_id.height", string="Height (cm)", readonly=True)
    acs_height_name = fields.Char(
        related="appointment_id.acs_height_name", string="Height Unit Label", readonly=True)
    temp = fields.Float(
        related="appointment_id.temp", string="Temperature (°C)", readonly=True)
    acs_temp_name = fields.Char(
        related="appointment_id.acs_temp_name", string="Temperature Unit Label", readonly=True)
    hr = fields.Integer(
        related="appointment_id.hr", string="Heart Rate (bpm)", readonly=True)
    rr = fields.Integer(
        related="appointment_id.rr", string="Respiratory Rate", readonly=True)
    systolic_bp = fields.Integer(
        related="appointment_id.systolic_bp", string="Systolic BP", readonly=True)
    diastolic_bp = fields.Integer(
        related="appointment_id.diastolic_bp", string="Diastolic BP", readonly=True)
    spo2 = fields.Integer(
        related="appointment_id.spo2", string="SpO2 (%)", readonly=True)
    acs_spo2_name = fields.Char(
        related="appointment_id.acs_spo2_name", string="SpO2 Unit Label", readonly=True)
    rbs = fields.Float(
        related="appointment_id.rbs", string="Random Blood Sugar (mg/dL)", readonly=True)
    acs_rbs_name = fields.Char(
        related="appointment_id.acs_rbs_name", string="RBS Unit Label", readonly=True)
    bmi = fields.Float(
        related="appointment_id.bmi", string="BMI", readonly=True)
    bmi_state = fields.Selection(
        related="appointment_id.bmi_state", string="BMI Category", readonly=True)
    pain_level = fields.Selection(
        related="appointment_id.pain_level", string="Pain Level", readonly=True)
    pain = fields.Selection(
        related="appointment_id.pain", string="Pain Description", readonly=True)
    lab_report = fields.Text(
        related="appointment_id.lab_report", string="Laboratory Report", readonly=True)
