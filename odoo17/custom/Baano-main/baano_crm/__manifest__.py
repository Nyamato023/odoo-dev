{
    'name': 'Baano CRM Customization',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Customizations for CRM module for Baano',
    'description': """
        This module overrides and customizes the standard CRM module to meet the specific requirements of Baano.
    """,
    'author': 'WanaagSolutions',
    'depends': ['crm', 'mail', 'crm_iap_mine', 'crm_sms', 'stock', 'hr', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/baano_target_views.xml',
        'views/crm_menus.xml',
        'views/crm_config_menus.xml',
        'views/config_lists_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
