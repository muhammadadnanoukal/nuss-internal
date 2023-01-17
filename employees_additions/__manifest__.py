# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Employees Additions',
    'version' : '1.0',
    'category': 'Responsibility Employee/Employee',
    'depends' : ['base','hr','documents', 'hr_contract', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/responsibility_views.xml',
        'views/generalizations_views.xml',
        'views/administrative_orders_views.xml',
        'views/extra_hr_views.xml',
        'views/proofs_views.xml',
        'views/specific_orders_views.xml',
        'views/personal_information.xml',
        'views/contract_addition_views.xml',
        'views/mission_views.xml',
        'views/followed_courses_views.xml',
        'views/leader_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}