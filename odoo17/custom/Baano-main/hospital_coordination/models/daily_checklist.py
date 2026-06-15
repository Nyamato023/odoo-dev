# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HospitalDailyChecklist(models.Model):
    _name = 'hospital.daily.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Daily Checklist'
    _order = 'date desc'
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    
    # Outreach Table
    line_ids = fields.One2many('hospital.daily.checklist.line', 'checklist_id', string='Hospitals Contacted')

    # Simple Text Inputs for Other Notebook Tabs
    doctor_notes = fields.Text(string='Doctor Profile Details')
    update_notes = fields.Text(string='Updates & Promos Details')
    complaint_notes = fields.Text(string='Complaints Details')
    challenge_notes = fields.Text(string='Collaboration Challenges')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.daily.checklist') or 'New'
        return super(HospitalDailyChecklist, self).create(vals_list)

    def action_print_report(self):
        return self.env.ref('hospital_coordination.action_report_daily_checklist').report_action(self)


class HospitalDailyChecklistLine(models.Model):
    _name = 'hospital.daily.checklist.line'
    _description = 'Hospital Daily Checklist Line'

    checklist_id = fields.Many2one('hospital.daily.checklist', string='Checklist', ondelete='cascade')
    hospital_id = fields.Many2one('x_hospitals', string='Hospital', required=True)
    notes = fields.Char(string='Notes')
