{
    'name': 'Manager Reports',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Custom reports for management',
    'author': 'Wanaag Solutions',
    'website': 'https://www.wanaagsolutions.com',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_report_views.xml',
        'reports/report_employee_progress.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
