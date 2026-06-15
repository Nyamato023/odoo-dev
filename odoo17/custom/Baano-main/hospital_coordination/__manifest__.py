# -*- coding: utf-8 -*-
{
    'name': 'Hospital Coordination',
    'version': '17.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Digitize daily and weekly hospital coordination checklists',
    'description': """
        Hospital Coordination Management for Baano.
        - Daily Operations Checklist
        - Weekly Strategic Checklist
        - Automated PDF Reporting
    """,
    'author': 'Wanaag Solutions',
    'website': 'https://www.wanaagsolutions.com',
    'depends': ['base', 'mail', 'web_studio'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/daily_checklist_views.xml',
        'report/daily_checklist_report.xml',
        'report/daily_checklist_template.xml',
        'report/weekly_checklist_report.xml',
        'report/weekly_checklist_template.xml',
        'views/weekly_checklist_views.xml',
        'views/customer_satisfaction_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
