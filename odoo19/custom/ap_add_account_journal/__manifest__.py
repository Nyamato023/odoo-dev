{
    'name': "AP add account journal",
    'summary': "Add journal items to invoices",
    'version': "19.0.1.0.0",
    'depends': ['account'],
    'author': "AP Accounting Services",
    'website': "http://www.ap-accounting.co.za",
    'category': 'Accounting',
    'description': """
        Add custom journal logic to invoices.
    """,
    'data': [
        'views/account_move.xml',
        'views/invoice_template.xml',
    ],
    'assets': {},
    'installable': True,
    'application': False,
    'auto_install': False,
}