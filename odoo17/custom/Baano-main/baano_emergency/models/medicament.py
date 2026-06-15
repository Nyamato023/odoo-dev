# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MedicamentGroup(models.Model):
    _name = 'medicament.group'
    _description = "Medicament Group"
    _order = 'name'

    name = fields.Char(string='Group Name', required=True, tracking=1)
    medicament_group_line_ids = fields.One2many(
        'medicament.group.line', 'group_id', string='Medicament Lines', copy=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)


class MedicamentGroupLine(models.Model):
    _name = 'medicament.group.line'
    _description = "Medicament Group Line"

    group_id = fields.Many2one(
        'medicament.group', string='Group', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Medicament', required=True,
                                 domain=[('hospital_product_type', '=', 'medicament')])
    common_dosage_id = fields.Many2one(
        'medicament.dosage', string='Dosage/Frequency')
    dose = fields.Float(string='Dosage', default=1.0)
    dosage_uom_id = fields.Many2one('uom.uom', string='Unit of Dosage')
    qty_per_day = fields.Float(string='Qty Per Day', default=1.0)
    days = fields.Float(string='Days', default=1.0)
    short_comment = fields.Char(string='Comment')
    allow_substitution = fields.Boolean(string='Allow Substitution')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
