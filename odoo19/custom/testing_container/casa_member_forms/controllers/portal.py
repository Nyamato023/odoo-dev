from odoo import http
from odoo.http import request


class MemberPortal(http.Controller):

    @http.route('/my/account/update', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def update_member_information(self, **post):

        partner = request.env.user.partner_id

        values = {
            "cipc_number": post.get("cipc_number"),
            "vat_number": post.get("vat_number"),
            "member_type": post.get("member_type"),
        }

        partner.write(values)

        return request.redirect("/my/account")