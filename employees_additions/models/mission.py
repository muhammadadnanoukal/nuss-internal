# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Mission(models.Model):
    _name = "mission.employee"
    _inherit = "mail.thread"

    name = fields.Char(string="المهمة")
    mission1 = fields.Many2one('hr.employee')
    # contents = fields.Html(required=True)
