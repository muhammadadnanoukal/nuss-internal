# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SpecificEmployee(models.Model):
    _inherit = "res.partner"
    # owner_of_relationship = fields.Many2one('decision.details', string='owner of the relationship')

    secondd = fields.Many2one('decision.details',string='second')
    thirdd = fields.Many2one('decision.details', string='third')
    forthh = fields.Many2one('decision.details', string='forth')
    fifthh = fields.Many2one('decision.details' ,string='fifth')
    sixthh = fields.Many2one('decision.details', string='sixth')
    seventhh = fields.Many2one('decision.details', string='seventh')