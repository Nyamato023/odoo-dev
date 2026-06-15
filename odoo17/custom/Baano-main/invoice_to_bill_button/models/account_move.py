from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    vendor_bill_id = fields.Many2one("account.move", string="Vendor Bill")
   
    hospital_id = fields.Many2one(
    "res.partner",
    domain="[('is_hospital','=',True)]"
)

    def action_create_vendor_bill(self):
        self.ensure_one()

        if self.vendor_bill_id:
            return  # Only one bill allowed

        # Copy invoice lines
        lines = []
        for line in self.invoice_line_ids:
            lines.append((0, 0, {
                "product_id": line.product_id.id,
                "name": line.name,
                "quantity": line.quantity,
                "price_unit": 0,  # manual entry
            }))

        # Create vendor bill with hospital as vendor
        bill = self.env["account.move"].create({
            "move_type": "in_invoice",
           "partner_id": self.hospital_id.id,
           "hospital_id": self.hospital_id.id,
            "invoice_origin": self.name,
            "invoice_line_ids": lines,
        })


        self.vendor_bill_id = bill.id

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": bill.id,
            "view_mode": "form",
        }

    def action_open_vendor_bill(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.vendor_bill_id.id,
            "view_mode": "form",
        }


    @api.onchange('hospital_id')
    def _onchange_hospital(self):
        for rec in self:
            if rec.move_type == 'in_invoice' and rec.hospital_id:
                rec.partner_id = rec.hospital_id.partner_id