{
    "name": "CASA New Member Application",
    "version": "19.0.1.0.0",
    "category": "Website/Website",
    "summary": "Public, staged and approval-driven CASA member onboarding",
    "author": "CASA",
    "license": "LGPL-3",
    "depends": ["auth_signup", "crm", "mail", "portal", "website"],
    "data": [
        "security/member_application_security.xml",
        "security/ir.model.access.csv",
        "data/member_application_sequence.xml",
        "data/member_application_mail_templates.xml",
        "views/res_partner_views.xml",
        "views/member_application_views.xml",
        "views/member_application_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "casa_member_application/static/src/js/member_application.js",
            "casa_member_application/static/src/scss/member_application.scss",
        ],
    },
    "application": True,
    "installable": True,
}
