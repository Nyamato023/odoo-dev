from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    membership_record_type = fields.Selection(
        [
            ("affiliate", "Member Affiliation"),
            ("entity", "Member Entity"),
            ("branch", "Member Branch"),
        ],
        index=True,
        copy=False,
    )
    legal_registered_name = fields.Char(string="Registered Name", copy=False)
    member_contact_name = fields.Char(string="Membership Contact", copy=False)
    member_suburb = fields.Char(string="Suburb", copy=False)
    member_cell = fields.Char(string="Cell Number", copy=False)
    mfsa_member_number = fields.Char(copy=False, index="btree_not_null")
    casa_member_number = fields.Char(copy=False, index="btree_not_null")
    pastel_account_number = fields.Char(copy=False, index="btree_not_null")
    cipc_registration_no = fields.Char(string="CIPC Registration No.", copy=False, index="btree_not_null")
    ncr_registration_no = fields.Char(string="NCR Registration No.", copy=False, index="btree_not_null")
    ncr_status = fields.Selection(
        [("active", "Active"), ("pending", "Pending"), ("suspended", "Suspended"), ("cancelled", "Cancelled")],
        string="NCR Status",
        copy=False,
    )
    nlr_registration_no = fields.Char(string="NLR / Other Registration", copy=False)
    date_last_member_update = fields.Date(string="Date of Last Update", copy=False, index=True)
