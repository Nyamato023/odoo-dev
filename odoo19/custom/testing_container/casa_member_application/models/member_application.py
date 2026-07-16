import hashlib
import hmac
import re
import secrets
from datetime import timedelta

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_normalize


CIPC_RE = re.compile(r"^\d{4}/\d{6}/\d{2}$")
NCR_RE = re.compile(r"^NCR(?:CP)?\d+$", re.IGNORECASE)
SA_PHONE_RE = re.compile(r"^(?:\+27|0)\d{9}$")


class CasaMemberApplication(models.Model):
    _name = "casa.member.application"
    _description = "CASA New Member Application"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    reference = fields.Char(default=lambda self: _("New"), readonly=True, copy=False, index=True)
    access_token = fields.Char(default=lambda self: secrets.token_urlsafe(32), readonly=True, copy=False, index=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("received", "Application Received"),
            ("review", "Under Review"),
            ("approved", "Approved"),
            ("declined", "Declined"),
        ],
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )
    current_page = fields.Integer(default=1, copy=False)
    otp_hash = fields.Char(copy=False, groups="casa_member_application.group_casa_membership_officer")
    otp_expiry = fields.Datetime(copy=False, groups="casa_member_application.group_casa_membership_officer")
    email_verified = fields.Boolean(copy=False, tracking=True)

    applicant_type = fields.Selection(
        [("with_branches", "Head office / affiliation with branches"), ("standalone", "Standalone / single-location lender")],
        required=True,
        tracking=True,
    )
    registered_name = fields.Char(required=True, tracking=True)
    trading_name = fields.Char(required=True, tracking=True)
    cipc_registration_no = fields.Char(string="CIPC Registration No.", required=True, tracking=True)
    contact_name = fields.Char(required=True)
    email = fields.Char(required=True, tracking=True)
    cell = fields.Char(required=True)

    ncr_registration_no = fields.Char(string="NCR Registration No.", tracking=True)
    ncr_status = fields.Selection(
        [("active", "Active"), ("pending", "Pending"), ("suspended", "Suspended"), ("cancelled", "Cancelled")],
        tracking=True,
    )
    nlr_registration_no = fields.Char(string="NLR / Other Registration")
    vat_number = fields.Char()

    street = fields.Char()
    street2 = fields.Char(string="Unit / Building")
    suburb = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string="Province", ondelete="restrict")
    zip = fields.Char(string="Postal Code")
    phone = fields.Char(string="Office Phone")
    website = fields.Char()

    branch_count = fields.Integer(default=1)
    provide_branches_later = fields.Boolean(string="Provide branch details later")
    branch_ids = fields.One2many("casa.member.application.branch", "application_id", string="Branches", copy=True)

    affiliation_option = fields.Selection(
        [("existing", "Existing affiliate"), ("other", "Other"), ("none", "None")],
        default="none",
        required=True,
    )
    affiliation_id = fields.Many2one(
        "res.partner",
        string="Existing Affiliate",
        domain="[('membership_record_type', '=', 'affiliate')]",
        ondelete="restrict",
    )
    affiliation_other = fields.Char(string="Other Affiliation")
    cipc_attachment_id = fields.Many2one("ir.attachment", string="CIPC Certificate", copy=False, ondelete="set null")
    ncr_attachment_id = fields.Many2one("ir.attachment", string="NCR Certificate", copy=False, ondelete="set null")
    id_attachment_id = fields.Many2one("ir.attachment", string="Identity Document", copy=False, ondelete="set null")
    popia_consent = fields.Boolean(string="POPIA Consent")
    declaration_accepted = fields.Boolean()
    signature_name = fields.Char(string="Declaration Signature")

    duplicate_warning = fields.Text(readonly=True, tracking=True)
    decline_reason = fields.Text(tracking=True)
    pastel_account_number = fields.Char(
        help="Enter the Pastel account created by the CASA team before approval.",
        tracking=True,
    )
    payment_terms_note = fields.Text(
        help="Payment terms included in the approval welcome email.",
        tracking=True,
    )
    invoice_attachment_id = fields.Many2one(
        "ir.attachment", string="Welcome Invoice", copy=False, ondelete="set null"
    )
    certificate_attachment_id = fields.Many2one(
        "ir.attachment", string="Membership Certificate", copy=False, ondelete="set null"
    )
    lead_id = fields.Many2one("crm.lead", readonly=True, copy=False)
    entity_partner_id = fields.Many2one("res.partner", string="Created Member Entity", readonly=True, copy=False)
    approved_date = fields.Date(readonly=True, copy=False)
    resume_url = fields.Char(compute="_compute_urls")
    portal_signup_url = fields.Char(compute="_compute_urls")

    _access_token_unique = models.Constraint(
        "UNIQUE(access_token)", "The application access token must be unique."
    )
    _reference_unique = models.Constraint(
        "UNIQUE(reference)", "The application reference must be unique."
    )
    _branch_count_positive = models.Constraint(
        "CHECK(branch_count >= 0)", "Branch count cannot be negative."
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("reference", _("New")) == _("New"):
                vals["reference"] = self.env["ir.sequence"].next_by_code("casa.member.application") or _("New")
            if vals.get("email"):
                vals["email"] = email_normalize(vals["email"]) or vals["email"].strip().lower()
        records = super().create(vals_list)
        for record in records:
            if not record.lead_id:
                lead = self.env["crm.lead"].sudo().create(
                    {
                        "name": _("New CASA member application: %s", record.trading_name or record.registered_name),
                        "type": "lead",
                        "contact_name": record.contact_name,
                        "email_from": record.email,
                        "phone": record.cell,
                        "description": _("Public application %s was started.", record.reference),
                    }
                )
                record.sudo().lead_id = lead
        return records

    @api.depends("access_token", "entity_partner_id")
    def _compute_urls(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        for record in self:
            record.resume_url = f"{base_url}/new-member/resume/{record.access_token}" if record.access_token else False
            record.portal_signup_url = False
            if record.entity_partner_id:
                record.portal_signup_url = record.entity_partner_id.sudo()._get_signup_url()

    def issue_otp(self):
        self.ensure_one()
        otp = f"{secrets.randbelow(1000000):06d}"
        self.sudo().write(
            {
                "otp_hash": hashlib.sha256(otp.encode()).hexdigest(),
                "otp_expiry": fields.Datetime.now() + timedelta(minutes=10),
                "email_verified": False,
            }
        )
        self.env.ref("casa_member_application.mail_template_member_application_otp").sudo().with_context(otp=otp).send_mail(
            self.id, force_send=True
        )
        return True

    def verify_otp(self, otp):
        self.ensure_one()
        candidate = hashlib.sha256((otp or "").strip().encode()).hexdigest()
        valid = bool(
            self.otp_hash
            and self.otp_expiry
            and self.otp_expiry >= fields.Datetime.now()
            and hmac.compare_digest(candidate, self.otp_hash)
        )
        if valid:
            self.sudo().write({"email_verified": True, "otp_hash": False, "otp_expiry": False})
        return valid

    def _submission_errors(self):
        self.ensure_one()
        errors = []
        if not self.email_verified:
            errors.append(_("The applicant email has not been verified."))
        if not CIPC_RE.match(self.cipc_registration_no or ""):
            errors.append(_("CIPC registration must use yyyy/nnnnnn/nn format."))
        if not SA_PHONE_RE.match(re.sub(r"[\s()-]", "", self.cell or "")):
            errors.append(_("Enter a valid South African cell number."))
        if not NCR_RE.match(self.ncr_registration_no or ""):
            errors.append(_("Enter a valid NCR registration number (for example NCRCP12345)."))
        if self.vat_number and (not self.vat_number.isdigit() or len(self.vat_number) != 10):
            errors.append(_("VAT number must contain exactly 10 digits."))
        if not self.zip or not self.zip.isdigit() or len(self.zip) != 4:
            errors.append(_("Postal code must contain exactly 4 digits."))
        if not SA_PHONE_RE.match(re.sub(r"[\s()-]", "", self.phone or "")):
            errors.append(_("Enter a valid South African office phone number."))
        if self.applicant_type == "with_branches" and not self.provide_branches_later:
            if self.branch_count < 1 or len(self.branch_ids) != self.branch_count:
                errors.append(_("Provide the requested number of branch records, or choose to provide them later."))
        if self.affiliation_option == "existing" and not self.affiliation_id:
            errors.append(_("Select an existing affiliate."))
        if self.affiliation_option == "other" and not self.affiliation_other:
            errors.append(_("Enter the other affiliation name."))
        if not (self.cipc_attachment_id and self.ncr_attachment_id and self.id_attachment_id):
            errors.append(_("CIPC certificate, NCR certificate and identity document are required."))
        if not self.popia_consent or not self.declaration_accepted or not self.signature_name:
            errors.append(_("POPIA consent, declaration acceptance and typed signature are required."))
        return errors

    def _check_duplicates(self):
        self.ensure_one()
        applications = self.sudo().search(
            [
                ("id", "!=", self.id),
                ("state", "!=", "declined"),
                "|",
                "|",
                ("cipc_registration_no", "=ilike", self.cipc_registration_no),
                ("ncr_registration_no", "=ilike", self.ncr_registration_no),
                ("trading_name", "=ilike", self.trading_name),
            ],
            limit=10,
        )
        partners = self.env["res.partner"].sudo().search(
            [
                "|",
                "|",
                ("cipc_registration_no", "=ilike", self.cipc_registration_no),
                ("ncr_registration_no", "=ilike", self.ncr_registration_no),
                ("name", "=ilike", self.trading_name),
            ],
            limit=10,
        )
        leads = self.env["crm.lead"].sudo().search(
            [
                ("id", "!=", self.lead_id.id),
                "|",
                "|",
                ("partner_name", "=ilike", self.trading_name),
                ("name", "=ilike", self.trading_name),
                ("email_from", "=ilike", self.email),
            ],
            limit=10,
        )
        warnings = []
        if applications:
            warnings.append(_("Possible applications: %s", ", ".join(applications.mapped("reference"))))
        if partners:
            warnings.append(_("Possible members: %s", ", ".join(partners.mapped("display_name"))))
        if leads:
            warnings.append(_("Possible leads: %s", ", ".join(leads.mapped("display_name"))))
        warning = "\n".join(warnings)
        self.sudo().write({"duplicate_warning": warning})
        return warning

    def action_submit(self):
        for record in self:
            if record.state != "draft":
                continue
            errors = record._submission_errors()
            if errors:
                raise ValidationError("\n".join(errors))
            record._check_duplicates()
            record.write({"state": "received", "current_page": 6})
            if record.lead_id:
                record.lead_id.sudo().write(
                    {"description": _("CASA application %s was submitted for review.", record.reference)}
                )
        return True

    def action_start_review(self):
        for record in self.filtered(lambda item: item.state == "received"):
            record.write({"state": "review"})
        return True

    def action_decline(self):
        for record in self:
            if not record.decline_reason:
                raise UserError(_("Enter a decline reason before declining the application."))
            record.write({"state": "declined"})
            if record.lead_id:
                record.lead_id.sudo().action_set_lost(lost_reason_id=False)
        return True

    def _get_or_create_affiliate(self):
        self.ensure_one()
        if self.affiliation_option == "existing":
            return self.affiliation_id
        if self.affiliation_option == "other":
            return self.env["res.partner"].sudo().create(
                {"name": self.affiliation_other, "is_company": True, "membership_record_type": "affiliate"}
            )
        return self.env["res.partner"]

    def _create_member_records(self):
        self.ensure_one()
        if self.entity_partner_id:
            return self.entity_partner_id
        affiliate = self._get_or_create_affiliate()
        entity = self.env["res.partner"].sudo().create(
            {
                "name": self.trading_name or self.registered_name,
                "legal_registered_name": self.registered_name,
                "member_contact_name": self.contact_name,
                "member_suburb": self.suburb,
                "is_company": True,
                "membership_record_type": "entity",
                "parent_id": affiliate.id or False,
                "email": self.email,
                "phone": self.phone,
                "member_cell": self.cell,
                "street": self.street,
                "street2": self.street2,
                "city": self.city,
                "state_id": self.state_id.id,
                "zip": self.zip,
                "website": self.website,
                "vat": self.vat_number or False,
                "cipc_registration_no": self.cipc_registration_no,
                "ncr_registration_no": self.ncr_registration_no,
                "ncr_status": self.ncr_status,
                "nlr_registration_no": self.nlr_registration_no,
                "mfsa_member_number": self.env["ir.sequence"].next_by_code("casa.member.mfsa"),
                "casa_member_number": self.env["ir.sequence"].next_by_code("casa.member.casa"),
                "pastel_account_number": self.pastel_account_number,
                "date_last_member_update": fields.Date.context_today(self),
            }
        )
        for branch in self.branch_ids:
            self.env["res.partner"].sudo().create(
                {
                    "name": branch.trading_name,
                    "member_contact_name": branch.contact_name,
                    "parent_id": entity.id,
                    "type": "other",
                    "membership_record_type": "branch",
                    "email": branch.email,
                    "phone": branch.phone,
                    "street": branch.street,
                    "street2": branch.street2,
                    "city": branch.city,
                    "state_id": branch.state_id.id,
                    "zip": branch.zip,
                }
            )
        self.sudo().entity_partner_id = entity
        return entity

    def _grant_portal_access(self, partner):
        self.ensure_one()
        portal_users = partner.with_context(active_test=False).user_ids.filtered(lambda user: user._is_portal())
        if portal_users:
            portal_users.sudo().write({"active": True})
            partner.sudo().signup_prepare()
            return portal_users[0]
        wizard = self.env["portal.wizard"].sudo().create({"partner_ids": [Command.link(partner.id)]})
        wizard.user_ids.action_grant_access()
        return wizard.user_ids.user_id

    def action_approve(self):
        for record in self:
            if record.state not in ("received", "review"):
                raise UserError(_("Only received or under-review applications can be approved."))
            if not record.pastel_account_number:
                raise UserError(_("Create and enter the Pastel account number before approval."))
            if not record.payment_terms_note or not record.invoice_attachment_id or not record.certificate_attachment_id:
                raise UserError(
                    _("Enter the payment terms and attach the welcome invoice and membership certificate before approval.")
                )
            errors = record._submission_errors()
            if errors:
                raise ValidationError("\n".join(errors))
            entity = record._create_member_records()
            record._grant_portal_access(entity)
            today = fields.Date.context_today(record)
            record.write({"state": "approved", "approved_date": today})
            if record.lead_id:
                record.lead_id.sudo().action_set_won()
        return True

    def write(self, vals):
        old_states = {record.id: record.state for record in self}
        result = super().write(vals)
        if "state" in vals:
            template_by_state = {
                "received": "mail_template_member_application_received",
                "review": "mail_template_member_application_review",
                "approved": "mail_template_member_application_approved",
                "declined": "mail_template_member_application_declined",
            }
            for record in self:
                if old_states.get(record.id) != record.state and record.state in template_by_state:
                    email_values = None
                    if record.state == "approved":
                        email_values = {
                            "attachment_ids": [
                                Command.set(
                                    (record.invoice_attachment_id | record.certificate_attachment_id).ids
                                )
                            ]
                        }
                    self.env.ref(f"casa_member_application.{template_by_state[record.state]}").sudo().send_mail(
                        record.id, force_send=True, email_values=email_values
                    )
        return result


class CasaMemberApplicationBranch(models.Model):
    _name = "casa.member.application.branch"
    _description = "CASA New Member Application Branch"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    application_id = fields.Many2one("casa.member.application", required=True, ondelete="cascade", index=True)
    trading_name = fields.Char(required=True)
    contact_name = fields.Char(required=True)
    email = fields.Char()
    phone = fields.Char(required=True)
    street = fields.Char(required=True)
    street2 = fields.Char()
    city = fields.Char(required=True)
    state_id = fields.Many2one("res.country.state", required=True, ondelete="restrict")
    zip = fields.Char(required=True)
