# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Diseases(models.Model):
    _name = 'baano.diseases'
    _description = 'Diseases'

    name = fields.Char(string="Disease", required=True)
