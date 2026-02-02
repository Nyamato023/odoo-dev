from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    shop_logo = fields.Binary(
        string='Shop Logo',
        help='Logo to display on receipts for this POS',
        attachment=True,
        copy=False
    )

    shop_logo_filename = fields.Char(
        string='Logo Filename',
        copy=False
    )

    # Inherit the copy method to handle logo copying
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        # Don't copy the logo by default
        default['shop_logo'] = False
        default['shop_logo_filename'] = False
        return super(PosConfig, self).copy(default)
