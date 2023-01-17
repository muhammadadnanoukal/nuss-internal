# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re
from werkzeug.urls import url_encode


class CreateDecisions(models.Model):
    _name = "create.decisions.new"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='أنواع القرارات')

    # first = fields.One2many('res.partner', 'firstt', string='first')
