# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re


class WorkSchedule(models.Model):
    _name = "work.schedule"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    name = fields.Char(string='اسم جدول الأعمال', readonly=True)
    sequence = fields.Integer(string='التسلسل', default=0)
    title = fields.Text(string="العنوان")
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
    # leave_with_an_excuse = fields.Many2many('hr.employee', string="تغيب بعذر كل من الزملاء")
    is_next_stage = fields.Boolean(compute='_compute_next_stage')

    parent_form = fields.Many2one('work.schedule.stage')

    # def _compute_sequence(self):
    #     self

    @api.model
    def create(self, vals):
        seq_num = self.env['ir.sequence'].next_by_code('sch.sch')
        print('seq num')
        print(seq_num)
        num = int(re.findall(r'\d+', seq_num)[0])
        vals['sequence'] = num
        vals['name'] = ' ' + seq_num + ' ' or _('New')
        result = super(WorkSchedule, self).create(vals)
        return result

    def _compute_next_stage(self):
        work_schedule_stage = self.env['work.schedule.stage'].search([('parent_form_id', '=', self.id)], limit=1,
                                                                     order='id')
        if work_schedule_stage:
            self.is_next_stage = True
        else:
            self.is_next_stage = False


    def create_next_stage(self):
        return {
            'name': _('محضر جلسة'),
            'type': 'ir.actions.act_window',
            'res_model': 'work.schedule.stage',
            'view_mode': 'form',
        }


    def action_view_next_stage(self):
        work_schedule_stage = self.env['work.schedule.stage'].search([('parent_form_id', '=', self.id)], limit=1,
                                                                     order='id')

        action = {
            'type': 'ir.actions.act_window',
            'name': _('محضر جلسة'),
            'res_model': 'work.schedule.stage',
            'view_mode': 'form',
            'res_id': work_schedule_stage.id
        }
        return action

    # def _compute_next_sequence(self):
    #     last_seq = self.env['work.schedule.stage'].search([('sequence', '=', self._onchange_sequence)])
    #



        # work_schedule_sequence = self.env['work.schedule.stage'].search([('sequence', '=', self.sequence)])
        # print(work_schedule_sequence)
        # if work_schedule_sequence:
        #     self.is_next_stage = True
        # else:
        #     self.is_next_stage = False

    # @api.depends("sequence")
    # def compute_contents(self):
    #     for result in self._compute_next_stage():
    #         result = self.next_by_code
    #         print(result)
    #     return result
    #
    #
