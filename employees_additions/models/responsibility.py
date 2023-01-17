# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Responsibility(models.Model):
    _name = "responsibility.employee"
    _inherit = "mail.thread"

    name = fields.Char(string="المسؤولية")
    responsibility1 = fields.Many2one('hr.employee', string="المسؤولية")
    # contents = fields.Html(required=True)
