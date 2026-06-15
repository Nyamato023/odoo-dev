# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Medicine(models.Model):
    _name = 'baano.medicine'
    _description = 'medicine'

    name = fields.Char(string="Medicine", required=True)
