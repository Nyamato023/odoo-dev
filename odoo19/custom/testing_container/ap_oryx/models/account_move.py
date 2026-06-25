from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    total_weight = fields.Float(
        string="Weight",
        compute="_compute_weight_volume",
        store=True,
    )

    total_volume = fields.Float(
        string="Volume",
        compute="_compute_weight_volume",
        store=True,
    )

    @api.depends(
        "product_id",
        "product_id.weight",
        "product_id.volume",
        "quantity",
    )
    def _compute_weight_volume(self):
        for line in self:
            line.total_weight = (
                line.product_id.weight * line.quantity
            )
            line.total_volume = (
                line.product_id.volume * line.quantity
            )

  
class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_total_qty = fields.Float(
        compute="_compute_invoice_totals",
        store=True,
    )

    invoice_total_weight = fields.Float(
        compute="_compute_invoice_totals",
        store=True,
    )

    invoice_total_volume = fields.Float(
        compute="_compute_invoice_totals",
        store=True,
    )

    @api.depends(
        "invoice_line_ids.quantity",
        "invoice_line_ids.total_weight",
        "invoice_line_ids.total_volume",
    )
    def _compute_invoice_totals(self):
        for move in self:
            lines = move.invoice_line_ids

            move.invoice_total_qty = sum(lines.mapped("quantity"))
            move.invoice_total_weight = sum(lines.mapped("total_weight"))
            move.invoice_total_volume = sum(lines.mapped("total_volume"))