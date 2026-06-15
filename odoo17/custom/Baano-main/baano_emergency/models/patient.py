# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
import datetime


class Patient(models.Model):
    _name = 'baano.patient'
    _description = 'Patient'
    _inherits = {'res.partner': 'partner_id'}
    _sql_constraints = [
        ('unique_company_id_number', 'unique(company_id_number)',
         'Company ID Number must be unique.')
    ]

    # Foreign key to res.partner (delegation)
    partner_id = fields.Many2one(
        'res.partner', string="Related Partner", required=True, ondelete='cascade')

    # Custom patient-specific fields
    patient_id = fields.Char(
        string="Patient ID",
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    birthday = fields.Date(string="Date of Birth")
    company_id_number = fields.Char(
        string="Company ID",
        required=True,
        copy=False,
        index=True
    )

    site_id = fields.Many2one(
    'baano.site',
    string="Site",
    required=False,
    )
    company_id = fields.Many2one(
        related='site_id.company_id',
        string="Company",
        store=True,
        readonly=True,
    )


     

    
    mobile = fields.Char(
        string="Mobile",
        required=True,
        copy=False,
        index=True
    )

    department_ids = fields.Many2many(
        comodel_name='baano.department',
        relation='baano_patient_department_rel',
        column1='patient_id',
        column2='department_id',
        string="Departments"
    )

    birthday = fields.Date(string="Date of Birth")
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        inverse="_inverse_age",
        store=True
    )

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                today = date.today()
                born = record.birthday
                record.age = today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day)
                )
            else:
                record.age = 0

    def _inverse_age(self):
        """ Calculate birthday based on age when age is set manually """
        for record in self:
            if record.age:
                today = date.today()
                # Approximate birthday by subtracting age years from today
                birth_year = today.year - record.age
                # Keep the month and day the same as today for simplicity
                record.birthday = date(birth_year, today.month, today.day)
            else:
                record.birthday = False

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender")

    @api.model
    def create(self, vals):
        """
        Override the create method to auto-generate a unique Patient ID
        using an Odoo sequence named 'baano.patient'.
        """
        if vals.get('patient_id', 'New') == 'New':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code(
                'baano.patient') or 'New'
        return super(Patient, self).create(vals)

    def test(self):
        pass

    def action_create_appointment(self):
        """ Open appointment form pre-filled with current patient and now as appointment date """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Appointment',
            'res_model': 'baano.appointment',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
                'default_appointment_date': fields.Datetime.now(),
            },
        }
