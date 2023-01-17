{
    'name': 'NUSS',
    'version': '1.0',
    'description': """NUSS needs""",
    'category': 'Productivity',
    'depends': ['base','mail','hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/work_schedule.xml',
        'views/work_schedule_stage.xml',
        'views/decision_template_views.xml',
        'views/decision_details_views.xml',
        'views/specific_employees.xml',
        'views/create_decisions_views.xml',
        'data/ir_sequence_data.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': -1,
}
