from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.contract'

    acting_indemnity = fields.Integer(string='تعويض تمثيل')
    retirement_salary_difference = fields.Integer(string='فرق راتب التقاعد')
    empty_indemnity = fields.Integer(string='تعويض تفرغ')
    responsibility_indemnity = fields.Integer(string='تعويض مسؤولية')
    move_indemnity = fields.Integer(string='تعويض انتقال')
    internet_indemnity = fields.Integer(string='تعويض انترنت(سيرف)')
    health_assurance = fields.Boolean(string='تأمين صحي')
