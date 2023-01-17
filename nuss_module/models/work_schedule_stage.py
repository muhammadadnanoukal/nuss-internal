# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re


class WorkSchedule(models.Model):
    _name = "work.schedule.stage"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _compute_name(self):
        name_current = self.env['work.schedule'].search([],
                                                      order='id desc', limit=1).name
        return name_current

    name_current = fields.Char(string='اسم جدول الأعمال', readonly=True, default=_compute_name)

    name = fields.Char(string="نوع المحضر", readonly=True, required=True, default=lambda self: _('New'))
    record_type = fields.Selection([
        ('type_1', 'محضر دوري'),
        ('type_2', 'محضر إستثنائي'),
    ], required=True, string='نوع المحضر')
    sequence = fields.Integer(default=0)

    def write(self, vals):
        print(self.new_field)
        return super(WorkSchedule, self).write(vals)


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            # if vals['record_type'] == 'type_1':
            #     seq_num = self.env['ir.sequence'].next_by_code('work.schedule.stage.type_1')
            #     num = int(re.findall(r'\d+', seq_num)[0])
            #     vals['sequence'] = num
            #     vals['name'] = ' ' + seq_num + ' ' + ' (محضر دوري) ' or _('New')
            if vals['record_type'] == 'type_2':
                seq_num = self.env['ir.sequence'].next_by_code('work.schedule.stage.type_2')
                num = int(re.findall(r'\d+', seq_num)[0])
                vals['sequence'] = num
                vals['name'] = ' ' + seq_num + ' ' + ' (محضر إستثنائي) ' or _('New')
        result = super(WorkSchedule, self).create(vals)

        return result


    # , default = lambda self: self.env['specific.employees'].search([])[0]

    headed = fields.Many2one('specific.employees', string="برئاسة")
    present = fields.One2many('specific.employees', 'presents', string="الحاضرون ضمن الجلسة")
    leave_without_an_excuse = fields.One2many('specific.employees', 'without_an_excuse',
                                              string="تغيب بدون عذر كل من الزملاء")
    leave_with_an_excuse = fields.One2many('specific.employees', 'with_an_excuse', string="تغيب بعذر كل من الزملاء")

    # @api.onchange("create")
    # def _onchange_sequence(self):
    #     attribute_num = []
    #     attribute_num.extend(self.sequence_result.ids)

    @api.onchange('headed', 'present', 'leave_without_an_excuse', 'leave_with_an_excuse')
    def _onchange_employees(self):
        excluded_ids = []
        excluded_ids.extend(self.headed.ids)
        excluded_ids.extend(self.present.ids)
        excluded_ids.extend(self.leave_without_an_excuse.ids)
        excluded_ids.extend(self.leave_with_an_excuse.ids)
        all_employees_ids = self.env['specific.employees'].search([]).mapped('id')
        employees_subtraction = [x for x in all_employees_ids if x not in excluded_ids]
        return {
            'domain': {
                'headed': [('id', 'in', employees_subtraction)],
                'present': [('id', 'in', employees_subtraction)],
                'leave_without_an_excuse': [('id', 'in', employees_subtraction)],
                'leave_with_an_excuse': [('id', 'in', employees_subtraction)]
            }
        }

    date = fields.Date(string="التاريخ")
    political_side = fields.Html(string="الجانب السياسي")
    organization_and_qualification = fields.Html(string="جانب التنظيم و التأهيل")
    higher_education_and_student_issues = fields.Html(string=" جانب التعليم العالي وقضايا الطلبة")
    special_education = fields.Html(string="جانب التعليم الخاص")
    culture_and_arts = fields.Html(string="جانب الثقافة والفنون")
    sports = fields.Html(string="جانب الرياضة")
    the_outer_branches = fields.Html(string="جانب الفروع الخارجية")
    technical_education = fields.Html(string="جانب التعليم التقاني")
    media_and_informatics = fields.Html(string="جانب الاعلام والمعلوماتية")
    volunteer_work_and_social_activities = fields.Html(string="جانب العمل التطوعي والأنشطة الاجتماعية")
    foreign_relations = fields.Html(string="جانب العلاقات الخارجية")
    new_role = fields.Html(string="ما يستجد من أمور")
    parent_form_id = fields.Many2one('work.schedule', store=True)
    linked_fields = fields.One2many('decision.details', 'parent_form')
    new_field = fields.Html(string="decision",compute="compute_decision_contents")

    @api.onchange('linked_fields')
    def _onchange_linked_fields(self):
        self.new_field = ''
        for rec in self.linked_fields:
            self.new_field = "{} {}".format(self.new_field, rec.contents)
        self.new_field.replace('</p><p>', '')

    @api.depends("linked_fields")
    def compute_decision_contents(self):
        result = ''
        for contents in self.linked_fields:
            print(contents.contents)
            result += contents.contents
        self.new_field = result







