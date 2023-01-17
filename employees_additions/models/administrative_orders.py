# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AdministrativeOrders(models.Model):
    _name = "administrative.orders"
    _inherit = ["mail.thread"]

    title = fields.Text(string="اوامر ادارية")
    employee = fields.One2many('hr.employee', 'employees', string='المورد البشري')
    # linked_employee_field = fields.One2many('hr.employee',related='employee', readonly=True)
    date = fields.Date(string='التاريخ')

    decision_type = fields.Many2one('specific.orders',
                                    string="امر اداري")

    contents = fields.Html(string="المحتوى")
