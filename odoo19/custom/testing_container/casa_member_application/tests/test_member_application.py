from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests import HttpCase, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCasaMemberApplication(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env["res.country"].search([("code", "=", "ZA")], limit=1)
        cls.state = cls.env["res.country.state"].search(
            [("country_id", "=", cls.country.id)], limit=1
        ) or cls.env["res.country.state"].create(
            {"name": "Test Province", "code": "TP", "country_id": cls.country.id}
        )

    def _attachment(self, name):
        return self.env["ir.attachment"].create(
            {"name": name, "datas": "dGVzdA==", "mimetype": "application/pdf"}
        )

    def _application(self, **overrides):
        values = {
            "applicant_type": "standalone",
            "registered_name": "Example Finance (Pty) Ltd",
            "trading_name": "Example Finance",
            "cipc_registration_no": "2026/123456/07",
            "contact_name": "Alex Applicant",
            "email": "alex@example.com",
            "cell": "0821234567",
            "email_verified": True,
            "ncr_registration_no": "NCRCP12345",
            "ncr_status": "active",
            "street": "1 Main Road",
            "suburb": "Central",
            "city": "Cape Town",
            "state_id": self.state.id,
            "zip": "8001",
            "phone": "0211234567",
            "affiliation_option": "none",
            "cipc_attachment_id": self._attachment("cipc.pdf").id,
            "ncr_attachment_id": self._attachment("ncr.pdf").id,
            "id_attachment_id": self._attachment("id.pdf").id,
            "popia_consent": True,
            "declaration_accepted": True,
            "signature_name": "Alex Applicant",
            "payment_terms_note": "Payment due within 30 days.",
            "invoice_attachment_id": self._attachment("invoice.pdf").id,
            "certificate_attachment_id": self._attachment("certificate.pdf").id,
        }
        values.update(overrides)
        return self.env["casa.member.application"].create(values)

    def test_submission_only_stages_application(self):
        application = self._application()
        application.action_submit()
        self.assertEqual(application.state, "received")
        self.assertFalse(application.entity_partner_id)

    def test_approval_creates_member_and_numbers(self):
        application = self._application(pastel_account_number="PA-1001")
        application.action_submit()
        application.action_start_review()
        application.action_approve()
        self.assertEqual(application.state, "approved")
        self.assertTrue(application.entity_partner_id.casa_member_number)
        self.assertTrue(application.entity_partner_id.mfsa_member_number)
        self.assertEqual(application.entity_partner_id.date_last_member_update, fields.Date.today())

    def test_pastel_account_required_for_approval(self):
        application = self._application()
        application.action_submit()
        with self.assertRaises(UserError):
            application.action_approve()

    def test_branch_reconciliation(self):
        application = self._application(
            applicant_type="with_branches",
            branch_count=1,
            branch_ids=[
                Command.create(
                    {
                        "trading_name": "Example Branch",
                        "contact_name": "Branch Contact",
                        "phone": "0111234567",
                        "street": "2 Branch Road",
                        "city": "Johannesburg",
                        "state_id": self.state.id,
                        "zip": "2000",
                    }
                )
            ],
        )
        self.assertFalse(application._submission_errors())

    def test_expired_otp_is_rejected(self):
        application = self._application(email_verified=False)
        application.write(
            {"otp_hash": "not-a-real-hash", "otp_expiry": fields.Datetime.now() - timedelta(minutes=1)}
        )
        self.assertFalse(application.verify_otp("123456"))


@tagged("post_install", "-at_install")
class TestCasaMemberApplicationWebsite(HttpCase):
    def test_public_start_page_renders(self):
        response = self.url_open("/new-member")
        self.assertEqual(response.status_code, 200)
        self.assertIn("New member application", response.text)
