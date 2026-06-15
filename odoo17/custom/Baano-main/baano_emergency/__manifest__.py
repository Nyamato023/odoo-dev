# -*- coding: utf-8 -*-

# ╔═══════════════════════════════════════════════════╗
# ║                                                   ║
# ║                                                   ║
# ║   _  _  _                                         ║
# ║  | || || |                                        ║
# ║  | || || | ____ ____   ____  ____  ____           ║
# ║  | ||_|| |/ _  |  _ \ / _  |/ _  |/ _  |          ║
# ║  | |___| ( ( | | | | ( ( | ( ( | ( ( | |          ║
# ║   \______|\_||_|_| |_|\_||_|\_||_|\_|| |          ║
# ║                                  (_____|          ║
# ║      _          _            _                    ║
# ║     | |        | |      _   (_)                   ║
# ║      \ \   ___ | |_   _| |_  _  ___  ____   ___   ║
# ║       \ \ / _ \| | | | |  _)| |/ _ \|  _ \ /___)  ║
# ║   _____) ) |_| | | |_| | |__| | |_| | | | |___ |  ║
# ║  (______/ \___/|_|\____|\___)_|\___/|_| |_(___/   ║
# ║                                                   ║
# ║		SOFTWARE DEVELOPED AND SUPPORTED BY         ║
# ║			   WANAAG SOLUTIONS LTD.               ║
# ║			COPYRIGHT (C) 2020 - TO DATE           ║
# ║			https://www.wanaag.co.ke               ║
# ║                                                   ║
# ║                                                   ║
# ╚═══════════════════════════════════════════════════╝


{
    'name': 'Baano Emergency',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Emergency management for patients in Baano system',
    'description': """
        This module manages emergency patient data, including registration,appointment,
        prescriptions, lab testing and reporting handling.
    """,
    'author': 'Wanaag Solutions',
    'website': 'https://wanaag.co.ke',
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/reports.xml',
        'wizard/pain_level.xml',
        'views/patient.xml',
        'views/vitals_evaluation.xml',
        'views/appointment.xml',
        'views/prescription.xml',
        'views/laboratory_request_view.xml',
        'views/laboratory_test_view.xml',
        'views/laboratory_sample_view.xml',
        'views/lab_result_view.xml',
        'views/res_users.xml',
        # 'views/res_partner_view.xml',
        # 'views/webclient_templates.xml',
        'views/menu_items_actions.xml',
        'report/reports.xml',
        'report/disease_report_template.xml',
        'report/lab_report_template.xml',
        'report/prescriptions_report_template.xml',
        'report/total_handled_cases_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'baano_emergency/static/src/js/report.js',
            # 'baano_emergency/static/src/js/pwa.js',
            'baano_emergency/static/src/xml/report_dashboard.xml',
        ],
        # 'web.assets_common': [
        #     'baano_emergency/static/src/pwa/manifest.json',
        #     'baano_emergency/static/src/js/service-worker.js',
        # ],

    },
    'images': ['static/description/icon.png'],
    'sequence': 0,
    'installable': True,
    'application': True,
    'auto_install': False,
}
