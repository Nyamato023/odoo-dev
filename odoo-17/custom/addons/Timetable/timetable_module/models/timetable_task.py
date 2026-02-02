# timetable_module/models/timetable_task.py
from odoo import models, fields, api
from datetime import timedelta

class TimetableTask(models.Model):
    """Model for main timetable tasks, integrable with calendar view."""

    _name = 'timetable.task'
    _description = 'Timetable Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # For tracking and activities

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    start_datetime = fields.Datetime(string='Start Time', required=True)
    duration = fields.Float(string='Duration (hours)', default=1.0, help='Duration in hours')
    end_datetime = fields.Datetime(string='End Time', compute='_compute_end_datetime', store=True)
    user_id = fields.Many2one('res.users', string='Assigned User', default=lambda self: self.env.user)
    subtask_ids = fields.One2many('timetable.subtask', 'task_id', string='Subtasks')
    color = fields.Integer(string='Color')  # For highlighting tasks in views
    project_task_id = fields.Many2one('project.task', string='Linked Project Task')
    is_link_projects = fields.Boolean(compute='_compute_is_link_projects')  # To control visibility based on config

    @api.depends('start_datetime', 'duration')
    def _compute_end_datetime(self):
        """Compute end datetime based on start and duration."""
        for record in self:
            if record.start_datetime:
                record.end_datetime = record.start_datetime + timedelta(hours=record.duration)
            else:
                record.end_datetime = False

    def _compute_is_link_projects(self):
        """Compute if project linking is enabled from config."""
        link_projects = self.env['ir.config_parameter'].sudo().get_param('timetable.link_projects', default=False)
        for record in self:
            record.is_link_projects = bool(link_projects)
