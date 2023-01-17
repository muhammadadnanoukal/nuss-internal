# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ReversEmployee(models.Model):
    _inherit = "hr.employee"
    # owner_of_relationship = fields.Many2one('decision.details', string='owner of the relationship')

    firstt = fields.Many2one('decision.details', string='first')

    def action_specific_decisions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Decision Type',
            'res_model': 'decision.details',
            'domain': [('owner_of_the_relationship', 'in', self.id)],
            'view_mode': 'tree,form',
        }

