# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ExtraHr(models.Model):
    _inherit = 'res.lang'

    hr_employee_id = fields.Many2one('hr.employee')