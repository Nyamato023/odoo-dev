# timetable_module/__manifest__.py
{
    'name': 'Timetable Module',
    'version': '1.0',
    'summary': 'Timetable integration using calendar view in Odoo 17',
    'description': """Module for managing timetables with tasks and subtasks, including security, coloring, and optional project linking.""",
    'author': '***',
    'depends': ['calendar', 'mail', 'project'],
    'data': [
        'security/timetable_security.xml',
        'security/ir.model.access.csv',
        'views/timetable_task_views.xml',
        # 'views/timetable_config_views.xml',
    ],
    'installable': True,
    'application': True,
}
