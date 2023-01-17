# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ContractAdditionsStage(models.Model):
    _inherit = "hr.contract.history"

    contract_addition_stage = fields.Many2many('responsibility.employee', 'title_new', string="المسؤولية")
