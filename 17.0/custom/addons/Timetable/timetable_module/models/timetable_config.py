# timetable_module/models/timetable_config.py
from odoo import models, fields

class TimetableConfigSettings(models.TransientModel):
    """Configuration settings for timetable module."""

    _inherit = 'res.config.settings'

    link_projects = fields.Boolean(
        string='Link with Projects',
        config_parameter='timetable.link_projects',
        help='If enabled, allows linking timetable tasks to project tasks.'
    )
