from odoo import fields, models


STATUS_SELECTION = [
    ("reinstated", "REINSTATED"),
    ("registered", "REGISTERED"),
    ("resigned", "RESIGNED"),
    ("opportunity", "OPPORTUNITY (Member growth)"),
    ("active", "ACTIVE"),
    ("suspended", "SUSPENDED (Bad Debt)"),
]


class APResPartner(models.Model):
    _inherit = "res.partner"

    # ---------------------------------
    # General / Company Details
    # ---------------------------------

    registered_name = fields.Char()

    trading_name = fields.Char()

    affiliation_name = fields.Char()

    branch_name = fields.Char()

    branches = fields.Char()

    entity_type = fields.Selection(
        [
            ("affiliation", "Affiliation"),
            ("member", "Member"),
            ("contact", "Contact"),
            ("branch", "Branch"),
            ("stakeholder", "Stakeholder"),
            ("service_provider", "Service Provider"),
        ],
        string="Type",
    )

    member_type = fields.Char()

    focus_areas = fields.Char()

    service_type = fields.Char()

    industry_involvement = fields.Char()

    business_size = fields.Char()

    

    # ---------------------------------
    # Registration Numbers
    # ---------------------------------

    cipc_number = fields.Char()

    vat_number = fields.Char()

    ncr_number = fields.Char()

    casa_number = fields.Char()

    mfsa_number = fields.Char()

    pastel_number = fields.Char()

    branch_number = fields.Char()

    # ---------------------------------
    # Status
    # ---------------------------------

    member_status = fields.Selection(
        STATUS_SELECTION,
        string="Member Status",
    )

    internal_status = fields.Selection(
        STATUS_SELECTION,
        string="Internal Status",
    )

    ncr_status = fields.Selection(
        STATUS_SELECTION,
        string="NCR Status",
    )

    # ---------------------------------
    # Address
    # ---------------------------------

    unit = fields.Char()

    building = fields.Char()

    suburb = fields.Char()

    province = fields.Char()

    postal_code = fields.Char()

    # ---------------------------------
    # Contact Details
    # ---------------------------------

    contact_person = fields.Char()

    job_description = fields.Char()

    office_number = fields.Char()

    office_contact_number = fields.Char()