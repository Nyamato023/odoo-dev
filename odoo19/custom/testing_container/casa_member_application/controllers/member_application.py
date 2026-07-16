import base64
import hmac
import re

from odoo import Command, _, fields, http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import email_normalize

from ..models.member_application import CIPC_RE, NCR_RE, SA_PHONE_RE


class CasaMemberApplicationController(http.Controller):
    def _application(self, token, draft_only=True):
        application = request.env["casa.member.application"].sudo().search([("access_token", "=", token)], limit=1)
        if not application or not hmac.compare_digest(application.access_token, token):
            return request.env["casa.member.application"]
        if draft_only and application.state != "draft":
            return request.env["casa.member.application"]
        return application

    def _form_values(self, application=None, errors=None, **extra):
        za = request.env["res.country"].sudo().search([("code", "=", "ZA")], limit=1)
        values = {
            "application": application,
            "errors": errors or [],
            "posted": {},
            "edit_mode": False,
            "states": request.env["res.country.state"].sudo().search([("country_id", "=", za.id)], order="name"),
            "affiliates": request.env["res.partner"].sudo().search(
                [("membership_record_type", "=", "affiliate")], order="name"
            ),
        }
        values.update(extra)
        return values

    @http.route("/new-member", type="http", auth="public", website=True, sitemap=True)
    def new_member(self, **kwargs):
        return request.render("casa_member_application.member_application_page_1", self._form_values())

    @http.route(
        "/new-member/<string:token>/page/1",
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
        csrf=True,
    )
    def edit_page_1(self, token, **post):
        application = self._application(token)
        if not application or not application.email_verified:
            return request.not_found()
        errors = []
        if request.httprequest.method == "POST":
            if not CIPC_RE.match(post.get("cipc_registration_no", "").strip()):
                errors.append(_("CIPC registration must use yyyy/nnnnnn/nn format."))
            required = ["applicant_type", "registered_name", "trading_name", "contact_name", "cell"]
            if any(not post.get(field_name, "").strip() for field_name in required):
                errors.append(_("Complete all required fields."))
            if not SA_PHONE_RE.match(re.sub(r"[\s()-]", "", post.get("cell", ""))):
                errors.append(_("Enter a valid South African cell number."))
            if not errors:
                application.sudo().write(
                    {
                        "applicant_type": post["applicant_type"],
                        "registered_name": post["registered_name"].strip(),
                        "trading_name": post["trading_name"].strip(),
                        "cipc_registration_no": post["cipc_registration_no"].strip(),
                        "contact_name": post["contact_name"].strip(),
                        "cell": post["cell"].strip(),
                    }
                )
                return request.redirect(f"/new-member/{token}/page/6")
        posted = {
            "email": application.email,
            "applicant_type": post.get("applicant_type", application.applicant_type),
            "registered_name": post.get("registered_name", application.registered_name),
            "trading_name": post.get("trading_name", application.trading_name),
            "cipc_registration_no": post.get("cipc_registration_no", application.cipc_registration_no),
            "contact_name": post.get("contact_name", application.contact_name),
            "cell": post.get("cell", application.cell),
        }
        return request.render(
            "casa_member_application.member_application_page_1",
            self._form_values(application, errors, posted=posted, edit_mode=True),
        )

    @http.route("/new-member/start", type="http", auth="public", website=True, methods=["POST"], csrf=True)
    def start(self, **post):
        errors = []
        normalized_email = email_normalize(post.get("email", ""))
        if not normalized_email:
            errors.append(_("Enter a valid email address."))
        if not CIPC_RE.match(post.get("cipc_registration_no", "").strip()):
            errors.append(_("CIPC registration must use yyyy/nnnnnn/nn format."))
        required = ["applicant_type", "registered_name", "trading_name", "contact_name", "cell"]
        if any(not post.get(field_name, "").strip() for field_name in required):
            errors.append(_("Complete all required fields."))
        if not SA_PHONE_RE.match(re.sub(r"[\s()-]", "", post.get("cell", ""))):
            errors.append(_("Enter a valid South African cell number."))
        if errors:
            return request.render(
                "casa_member_application.member_application_page_1",
                self._form_values(errors=errors, posted=post),
            )
        application = request.env["casa.member.application"].sudo().create(
            {
                "applicant_type": post["applicant_type"],
                "registered_name": post["registered_name"].strip(),
                "trading_name": post["trading_name"].strip(),
                "cipc_registration_no": post["cipc_registration_no"].strip(),
                "contact_name": post["contact_name"].strip(),
                "email": normalized_email,
                "cell": post["cell"].strip(),
            }
        )
        application.issue_otp()
        return request.redirect(f"/new-member/verify/{application.access_token}")

    @http.route("/new-member/verify/<string:token>", type="http", auth="public", website=True, methods=["GET", "POST"])
    def verify(self, token, **post):
        application = self._application(token)
        if not application:
            return request.not_found()
        errors = []
        if request.httprequest.method == "POST":
            if post.get("resend"):
                application.issue_otp()
            elif application.verify_otp(post.get("otp")):
                return request.redirect(f"/new-member/{token}/page/2")
            else:
                errors.append(_("The OTP is incorrect or has expired."))
        return request.render(
            "casa_member_application.member_application_verify",
            self._form_values(application, errors),
        )

    @http.route("/new-member/resume/<string:token>", type="http", auth="public", website=True)
    def resume(self, token, **kwargs):
        application = self._application(token, draft_only=False)
        if not application:
            return request.not_found()
        if application.state != "draft":
            return request.render(
                "casa_member_application.member_application_complete",
                self._form_values(application),
            )
        if not application.email_verified:
            application.issue_otp()
            return request.redirect(f"/new-member/verify/{token}")
        return request.redirect(f"/new-member/{token}/page/{max(2, application.current_page)}")

    @http.route(
        "/new-member/<string:token>/page/<int:page>",
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
        csrf=True,
    )
    def page(self, token, page, **post):
        application = self._application(token)
        if not application or not application.email_verified or page not in (2, 3, 4, 5, 6):
            return request.not_found()
        errors = []
        if request.httprequest.method == "POST":
            try:
                if page == 2:
                    errors = self._save_page_2(application, post)
                elif page == 3:
                    errors = self._save_page_3(application, post)
                elif page == 4:
                    errors = self._save_page_4(application, post)
                elif page == 5:
                    errors = self._save_page_5(application, post)
                elif page == 6:
                    application.action_submit()
                    return request.redirect(f"/new-member/resume/{token}")
                if not errors:
                    next_page = page + 1
                    if next_page == 4 and application.applicant_type == "standalone":
                        next_page = 5
                    application.sudo().current_page = next_page
                    return request.redirect(f"/new-member/{token}/page/{next_page}")
            except ValidationError as error:
                errors.append(error.args[0])
        template = f"casa_member_application.member_application_page_{page}"
        return request.render(template, self._form_values(application, errors, branch_count=max(application.branch_count, 1)))

    def _save_page_2(self, application, post):
        errors = []
        ncr = post.get("ncr_registration_no", "").strip()
        if not NCR_RE.match(ncr):
            errors.append(_("Enter a valid NCR registration number (for example NCRCP12345)."))
        if post.get("ncr_status") not in {"active", "pending", "suspended", "cancelled"}:
            errors.append(_("Select the NCR status."))
        vat = re.sub(r"\s+", "", post.get("vat_number", ""))
        if vat and (not vat.isdigit() or len(vat) != 10):
            errors.append(_("VAT number must contain exactly 10 digits."))
        if not errors:
            application.sudo().write(
                {
                    "ncr_registration_no": ncr.upper(),
                    "ncr_status": post["ncr_status"],
                    "nlr_registration_no": post.get("nlr_registration_no", "").strip(),
                    "vat_number": vat,
                }
            )
        return errors

    def _save_page_3(self, application, post):
        errors = []
        state = request.env["res.country.state"].sudo().browse(int(post.get("state_id", 0) or 0)).exists()
        zip_code = post.get("zip", "").strip()
        for field_name in ("street", "suburb", "city", "phone"):
            if not post.get(field_name, "").strip():
                errors.append(_("Complete all required address and contact fields."))
                break
        if not state:
            errors.append(_("Select a province."))
        if not zip_code.isdigit() or len(zip_code) != 4:
            errors.append(_("Postal code must contain exactly 4 digits."))
        if not SA_PHONE_RE.match(re.sub(r"[\s()-]", "", post.get("phone", ""))):
            errors.append(_("Enter a valid South African office phone number."))
        if not errors:
            application.sudo().write(
                {
                    "street": post["street"].strip(),
                    "street2": post.get("street2", "").strip(),
                    "suburb": post["suburb"].strip(),
                    "city": post["city"].strip(),
                    "state_id": state.id,
                    "zip": zip_code,
                    "phone": post["phone"].strip(),
                    "website": post.get("website", "").strip(),
                }
            )
        return errors

    def _save_page_4(self, application, post):
        if application.applicant_type == "standalone":
            application.sudo().write({"branch_count": 0, "branch_ids": [Command.clear()]})
            return []
        provide_later = bool(post.get("provide_branches_later"))
        count = int(post.get("branch_count", 0) or 0)
        errors = []
        if count < 1:
            errors.append(_("Branch count must be at least one."))
        commands = [Command.clear()]
        if not provide_later:
            for index in range(count):
                prefix = f"branch_{index}_"
                state = request.env["res.country.state"].sudo().browse(int(post.get(prefix + "state_id", 0) or 0)).exists()
                required = ["trading_name", "contact_name", "phone", "street", "city", "zip"]
                if any(not post.get(prefix + name, "").strip() for name in required) or not state:
                    errors.append(_("Complete all required fields for branch %s.", index + 1))
                    continue
                branch_phone = re.sub(r"[\s()-]", "", post[prefix + "phone"])
                branch_zip = post[prefix + "zip"].strip()
                if not SA_PHONE_RE.match(branch_phone) or not branch_zip.isdigit() or len(branch_zip) != 4:
                    errors.append(_("Enter a valid South African phone and 4-digit postal code for branch %s.", index + 1))
                    continue
                commands.append(
                    Command.create(
                        {
                            "sequence": (index + 1) * 10,
                            "trading_name": post[prefix + "trading_name"].strip(),
                            "contact_name": post[prefix + "contact_name"].strip(),
                            "email": post.get(prefix + "email", "").strip(),
                            "phone": post[prefix + "phone"].strip(),
                            "street": post[prefix + "street"].strip(),
                            "street2": post.get(prefix + "street2", "").strip(),
                            "city": post[prefix + "city"].strip(),
                            "state_id": state.id,
                            "zip": post[prefix + "zip"].strip(),
                        }
                    )
                )
        if not errors:
            application.sudo().write(
                {"branch_count": count, "provide_branches_later": provide_later, "branch_ids": commands}
            )
        return errors

    def _store_upload(self, application, field_name, upload, label):
        if not upload or not upload.filename:
            return False
        data = upload.read(10 * 1024 * 1024 + 1)
        if len(data) > 10 * 1024 * 1024:
            raise ValidationError(_("%s must be 10 MB or smaller.", label))
        allowed = {"application/pdf", "image/jpeg", "image/png", "image/heic", "image/heif"}
        if upload.mimetype not in allowed:
            raise ValidationError(_("%s must be a PDF or supported phone image.", label))
        old = application[field_name]
        attachment = request.env["ir.attachment"].sudo().create(
            {
                "name": upload.filename,
                "datas": base64.b64encode(data),
                "mimetype": upload.mimetype,
                "res_model": application._name,
                "res_id": application.id,
            }
        )
        application.sudo().write({field_name: attachment.id})
        if old:
            old.sudo().unlink()
        return attachment

    def _save_page_5(self, application, post):
        errors = []
        option = post.get("affiliation_option")
        if option not in {"existing", "other", "none"}:
            errors.append(_("Select a membership affiliation option."))
        affiliate = request.env["res.partner"]
        if option == "existing":
            affiliate = request.env["res.partner"].sudo().browse(int(post.get("affiliation_id", 0) or 0)).exists()
            if not affiliate or affiliate.membership_record_type != "affiliate":
                errors.append(_("Select a valid existing affiliate."))
        if option == "other" and not post.get("affiliation_other", "").strip():
            errors.append(_("Enter the other affiliation name."))
        if not post.get("popia_consent") or not post.get("declaration_accepted") or not post.get("signature_name", "").strip():
            errors.append(_("Accept the POPIA consent and declaration, then type your full name."))
        uploads = request.httprequest.files
        for upload_name, field_name, label in (
            ("cipc_document", "cipc_attachment_id", _("CIPC certificate")),
            ("ncr_document", "ncr_attachment_id", _("NCR certificate")),
            ("id_document", "id_attachment_id", _("identity document")),
        ):
            if not uploads.get(upload_name) and not application[field_name]:
                errors.append(_("Upload the %s.", label))
        if errors:
            return errors
        application.sudo().write(
            {
                "affiliation_option": option,
                "affiliation_id": affiliate.id or False,
                "affiliation_other": post.get("affiliation_other", "").strip(),
                "popia_consent": True,
                "declaration_accepted": True,
                "signature_name": post["signature_name"].strip(),
            }
        )
        self._store_upload(application, "cipc_attachment_id", uploads.get("cipc_document"), _("CIPC certificate"))
        self._store_upload(application, "ncr_attachment_id", uploads.get("ncr_document"), _("NCR certificate"))
        self._store_upload(application, "id_attachment_id", uploads.get("id_document"), _("identity document"))
        return []
