from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

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
        "product_uom_qty",
    )
    def _compute_weight_volume(self):
        for line in self:
            line.total_weight = (
                line.product_id.weight * line.product_uom_qty
            )
            line.total_volume = (
                line.product_id.volume * line.product_uom_qty
            )