{
    'name': 'POS Shop Logo',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Add custom shop logo to POS configuration',
    'description': """
        This module adds a shop logo field to POS configuration.
        The logo will be used on receipts for sessions in this POS.
    """,
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
