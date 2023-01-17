# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ExtraHr(models.Model):
    _inherit = ["hr.employee"]

    social_security = fields.Selection([
        ('type_1', 'مشترك'),
        ('type_2', 'غير مشترك'),
    ], string='الضمان الإجتماعي')

    number_social = fields.Integer(string="رقم الضمان الاجتماعي")
    date = fields.Date(string="التاريخ")
    date_of_close = fields.Date(string="تاريخ الإنفكاك")

    medical_insurance = fields.Selection([
        ('type_1', 'مشترك'),
        ('type_2', 'غير مشترك'),
    ], string='الضمان الصحي')

    number_of_medical = fields.Integer(string="رقم الضمان الصحي", required=True)
    date_of_start = fields.Date(string="تاريخ البداية")
    date_of_end = fields.Date(string="تاريخ النهاية")





