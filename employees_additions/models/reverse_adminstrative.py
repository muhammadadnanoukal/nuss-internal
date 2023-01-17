# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Generalizations(models.Model):
    _inherit = ["hr.employee"]

    employees = fields.Many2one('administrative.orders',string="employee")
    employees1 = fields.Many2one('followed.courses')

