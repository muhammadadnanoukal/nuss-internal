# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ContractAdditions(models.Model):
    _inherit = "hr.contract"

    contract_addition = fields.Many2many('responsibility.employee', 'title_new', string="المسؤولية")

