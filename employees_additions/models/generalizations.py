# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Generalizations(models.Model):
    _name = "generalizations.employee"
    _inherit = ["mail.thread"]

    title = fields.Text(string="المسؤولية")
    date = fields.Date(string='التاريخ', required=True)
    contents = fields.Html(string="المحتوى")