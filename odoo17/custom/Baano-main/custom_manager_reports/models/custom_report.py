from odoo import models, fields, api

class CustomManagerReport(models.Model):
    _name = 'custom.manager.report'
    _description = 'Custom Manager Report' 
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Report Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    employee_id = fields.Many2one('hr.employee', string='Employee Name', required=True, tracking=True)
    job_id = fields.Many2one('hr.job', string='Job Position', related='employee_id.job_id', readonly=True, store=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', readonly=True, store=True, tracking=True)
    
    date_from = fields.Date(string='From', tracking=True, required=True)
    date_to = fields.Date(string='To', tracking=True, required=True)
    
    state = fields.Selection([
        ('first', 'First Status'),
        ('second', 'Second Status'),
        ('third', 'Third Status')
    ], string='Status', default='first', tracking=True)

    challenges_faced = fields.Text(string='Challenges Faced')
    recommendations = fields.Text(string='Recommendations')
    line_ids = fields.One2many('custom.manager.report.line', 'report_id', string='Tasks')
    
    day1_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day1')], string='Day 1')
    day2_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day2')], string='Day 2')
    day3_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day3')], string='Day 3')
    day4_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day4')], string='Day 4')
    day5_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day5')], string='Day 5')
    day6_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day6')], string='Day 6')
    day7_line_ids = fields.One2many('custom.manager.report.line', 'report_id', domain=[('day', '=', 'day7')], string='Day 7')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('custom.manager.report') or 'New'
        return super(CustomManagerReport, self).create(vals_list)

class CustomManagerReportLine(models.Model):
    _name = 'custom.manager.report.line'
    _description = 'Custom Manager Report Line'

    report_id = fields.Many2one('custom.manager.report', string='Report', ondelete='cascade')
    day = fields.Selection([
        ('day1', 'Day 1'),
        ('day2', 'Day 2'),
        ('day3', 'Day 3'),
        ('day4', 'Day 4'),
        ('day5', 'Day 5'),
        ('day6', 'Day 6'),
        ('day7', 'Day 7'),
    ], string='Day')
    name = fields.Char(string='Tasks', required=True)

