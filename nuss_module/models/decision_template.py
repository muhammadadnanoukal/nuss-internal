# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re


class Forms(models.Model):
    _name = "decision.template"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="العنوان")
    decision_type = fields.Selection([
        ('type_1', 'قرارات جلسة'),
        ('type_2', 'قرارات لجنة رباعية'),
    ], required=True, string='النوع')
    content = fields.Html(string='المحتوى', required=True, store=True, readonly=False)
    sequence = fields.Integer(default=0)

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('رقم')) == _('رقم'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('kalb.kalb')
    #     result = super(Forms, self).create(vals)
    #     return result
