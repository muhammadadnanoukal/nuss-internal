# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FollowedCourses(models.Model):
    _name = "followed.courses"
    _inherit = ["mail.thread"]

    title = fields.Text(required=True, string="الدورات المتبعة")
    employee = fields.One2many('hr.employee', 'employees1', string='المورد البشري')
    date = fields.Date(string='التاريخ')
    file = fields.Binary(string='رفع ملف')

    @api.onchange('file')
    def check_file(self):
        if self.file:
            vals1 = {
                'name': 'الدورات المتبعة'
            }
            result = self.env['documents.folder'].search([('name', '=', 'الدورات المتبعة')])
            if not result:
                result = self.env['documents.folder'].create(vals1)
            vals = {
                'datas': self.file,
                'name': self.title,
                'folder_id': result.id
            }
            self.env['documents.document'].create(vals)
