from odoo import models, fields


class Leader(models.AbstractModel):
    _inherit = ["hr.employee.base"]
    # employee_type = fields.Selection([
    #     ('employee', 'Employee'),
    #     ('leader', 'قيادي'),
    #     ('student', 'Student'),
    #     ('trainee', 'Trainee'),
    #     ('contractor', 'Contractor'),
    #     ('freelance', 'Freelancer'),
    # ], string='Employee Type', default='employee', required=True,
    #     help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")

    mission = fields.One2many('mission.employee', 'mission1', string="المهمة")
    responsibility = fields.One2many('responsibility.employee', 'responsibility1', string="المسؤولية")