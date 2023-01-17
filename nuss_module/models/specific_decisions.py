# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SpecificDecisions(models.Model):
    _name = "specific.decisions.same"

    name = fields.Char(string='القرارات')
    decision = fields.Many2one("create.decisions.new",string="انواع القرارات")
