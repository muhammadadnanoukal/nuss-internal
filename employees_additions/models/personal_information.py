# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PersonalInformation(models.Model):
    _inherit = "hr.employee"

    id_number = fields.Integer(string='رقم الهوية')
    National_number = fields.Integer(string='رقم الوطني')
    first_name = fields.Char(string='الاسم الأول')
    last_name = fields.Char(string='الكنية')
    father_name = fields.Char(string='اسم الأب')
    mothers_first_and_last_name = fields.Char(string='اسم الأم والكنية')
    alAmaneh = fields.Char(string='الأمانة')
    mkanAlKied = fields.Char(string='مكان القيد')
    raamAlkhana = fields.Integer(string='رقم الخانة')
    ##################################################
    husbendsWork = fields.Char(string='عمل الزوج')
    childrenNum = fields.Integer(string='عدد الأولاد')
    sex = fields.Selection(string='الجنس',
                           selection=[
                               ("male", "ذكر"),
                               ("female", "انثى"),
                           ], default='male')
    dateOfBirth = fields.Date(string='تاريخ الميلاد')
    educationalCertificates = fields.Selection(string='الشهادات التعليمية',
                                               selection=[
                                                   ("ابتدائي", "ابتدائي"),
                                                   ("اعدادي", "اعدادي"),
                                                   ("ثانوي", "ثانوي"),
                                                   ("معهد", "معهد"),
                                                   ("بكالوريوس", "بكالوريوس"),
                                                   ("ماجستير", "ماجستير"),
                                                   ("دكتوراه", "دكتوراه"),
                                               ], default='ثانوي')
    languages = fields.One2many('res.lang', 'hr_employee_id', string='اللغات',
                                domain="['|', ('active', '=', False), ('active', '=', True)]")

    child_sex_1 = fields.Selection(string='جنس الولد الأول',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_1 = fields.Date(string='تاريخ ميلاد الولد الأول')

    child_sex_2 = fields.Selection(string='جنس الولد الثاني',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_2 = fields.Date(string='تاريخ ميلاد الولد الثاني')

    child_sex_3 = fields.Selection(string='جنس الولد الثالث',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_3 = fields.Date(string='تاريخ ميلاد الولد الثالث')

    child_sex_4 = fields.Selection(string='جنس الولد الرابع',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_4 = fields.Date(string='تاريخ ميلاد الولد الرابع')

    child_sex_5 = fields.Selection(string='جنس الولد الخامس',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_5 = fields.Date(string='تاريخ ميلاد الولد الخامس')

    child_sex_6 = fields.Selection(string='جنس الولد السادس',
                                   selection=[
                                       ("male", "ذكر"),
                                       ("female", "انثى"),
                                   ], default='male')
    child_birth_Date_6 = fields.Date(string='تاريخ ميلاد الولد السادس')

    def action_administrative_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Administrative Orders',
            'res_model': 'administrative.orders',
            'domain': [('employee', 'in', self.id)],
            'view_mode': 'tree,form',
        }

    @api.onchange('childrenNum')
    def _check_length(self):
        if self.childrenNum < 0:
            self.childrenNum = 0
        elif self.childrenNum > 6:
            self.childrenNum = 6
