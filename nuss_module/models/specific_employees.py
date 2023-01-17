# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SpecificEmployees(models.Model):
    _name = "specific.employees"

    name = fields.Many2one("hr.employee",string='اسماء الحاضرين في الاجتماع')
    presents = fields.Many2one('work.schedule.stage', string='الحاضرون ضمن الجلسة')
    without_an_excuse = fields.Many2one('work.schedule.stage', string='تغيب بدون عذر كل من الزملاء')
    with_an_excuse = fields.Many2one('work.schedule.stage', string='تغيب بعذر كل من الزملاء')

