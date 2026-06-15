# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HospitalWeeklyChecklist(models.Model):
    _name = 'hospital.weekly.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Weekly Checklist'
    _order = 'from_date desc'
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: 'New')
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)

    # Simplified Text Inputs for Weekly Tasks
    booking_performance = fields.Text(string='Booking Performance (Low vs High)')
    feedback_problems = fields.Text(string='Complaints & Collaboration Issues')
    promotions_campaigns = fields.Text(string='Active Promotions & Campaigns')
    insights_recommendations = fields.Text(string='Insights & Recommendations')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.weekly.checklist') or 'New'
        return super(HospitalWeeklyChecklist, self).create(vals_list)

    def action_print_report(self):
        # Trigger the PDF report generation
        return self.env.ref('hospital_coordination.action_report_weekly_checklist').report_action(self)
