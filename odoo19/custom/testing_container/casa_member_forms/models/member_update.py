from odoo import fields, models


STATUS_SELECTION = [
    ("reinstated", "REINSTATED"),
    ("registered", "REGISTERED"),
    ("resigned", "RESIGNED"),
    ("opportunity", "OPPORTUNITY (Member growth)"),
    ("active", "ACTIVE"),
    ("suspended", "SUSPENDED (Bad Debt)"),
]


class MemberUpdateLine(models.Model):
    _name = "member.update"
    _description = "Member Update Line"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)


    partner_id = fields.Many2one(
        "res.partner",
        string="Original Record",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("under_review", "Under Review"),
            ("approved", "Approved"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # Record Type
    type = fields.Selection(
        [
            ("affiliation", "Affiliation"),
            ("entity", "Member Entity"),
            ("branch", "Branch"),
            ("contact", "Contact"),
        ],
        required=True,
    )

    active = fields.Boolean(default=True)

    # -------------------------
    # General / Company Details
    # -------------------------

    registered_name = fields.Char()

    trading_name = fields.Char()

    affiliation_name = fields.Char()

    branch_name = fields.Char()

    branches = fields.Char()

    member_type = fields.Char()

    # -------------------------
    # Registration Numbers
    # -------------------------

    cipc_number = fields.Char()

    vat_number = fields.Char()

    ncr_number = fields.Char()

    casa_number = fields.Char()

    mfsa_number = fields.Char()

    pastel_number = fields.Char()

    branch_number = fields.Char()

    # -------------------------
    # Status
    # -------------------------

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

    # -------------------------
    # Address
    # -------------------------

    unit = fields.Char()

    building = fields.Char()

    street = fields.Char()

    suburb = fields.Char()

    city = fields.Char()

    province = fields.Char()

    postal_code = fields.Char()

    # -------------------------
    # Contact Details
    # -------------------------

    contact_person = fields.Char()

    job_description = fields.Char()

    office_number = fields.Char()

    office_contact_number = fields.Char()

    mobile_number = fields.Char()

    email = fields.Char()

    phone = fields.Char()

    def action_submit(self):
        self.write({
            "state": "under_review",
        })


    def action_approve(self):
        self.write({
            "state": "approved",
        })


    def action_reset_to_draft(self):
        self.write({
            "state": "draft",
        })

        # testing res_partner

class ResPartner(models.Model):
    _inherit = "res.partner"

    cipc_number = fields.Char()
    vat_number = fields.Char()
    member_type = fields.Char()