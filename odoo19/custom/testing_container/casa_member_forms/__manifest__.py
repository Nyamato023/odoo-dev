# -*- coding: utf-8 -*-

{
    "name": "CASA Member Information Update",
    "version": "19.0.1.0.0",
    "summary": "Online Member Information Update Portal",
    "description": """
CASA Member Information Update Portal

This module aims to provide a secure multi-step website portal for members to:

* Login using OTP
* Complete annual member information updates
* Verify affiliation details
* Verify linked entities
* Verify branch information
* Submit changes for approval
* Track approval status

The module stages all submitted information before updating the live
member records.
    """,
    "author": "AP Systems",
    "category": "Website/Portal",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "mail",
        "portal",
        "website",
    ],
    "data": [
        # Security
        # "security/security.xml",
        "security/ir.model.access.csv",

        # Data
        # "data/sequence.xml",
        # "data/mail_template.xml",

        # Views
        "views/member_update_views.xml",
        "views/ap_res_partner_views.xml",
   
        # Website
        "data/website_templates.xml",

        # Menus
        "views/menu.xml",
    ],
   
    "application": True,
    "installable": True,
    "auto_install": False,
}