# -*- coding: utf-8 -*-
from odoo import models, fields


class CustomerSatisfaction(models.Model):
    _name = 'hospital.customer.satisfaction'
    _description = 'Customer Satisfaction'

    description = fields.Text(string='Description')
