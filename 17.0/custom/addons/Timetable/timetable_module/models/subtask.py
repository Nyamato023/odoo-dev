# timetable_module/models/subtask.py
from odoo import models, fields

class TimetableSubtask(models.Model):
    """Model for subtasks under main timetable tasks."""

    _name = 'timetable.subtask'
    _description = 'Timetable Subtask'

    name = fields.Char(string='Subtask Name', required=True)
    description = fields.Text(string='Description')
    task_id = fields.Many2one('timetable.task', string='Parent Task', required=True, ondelete='cascade')
