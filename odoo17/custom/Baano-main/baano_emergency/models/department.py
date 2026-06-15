# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Department(models.Model):
    _name = 'baano.department'
    _description = 'Department'

    name = fields.Char(string="Department Name", required=True)
