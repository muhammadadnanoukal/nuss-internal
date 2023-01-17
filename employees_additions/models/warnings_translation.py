# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
import logging
import random

from collections import defaultdict
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, Command, fields, models, _
from odoo.osv.expression import AND
from odoo.tools.misc import format_date

from server.odoo.exceptions import AccessError


class WarningsTranslation(models.Model):
    _inherit = ["hr.payslip"]

    @api.model
    def get_payroll_dashboard_data(self, sections=None):
        # Entry point for getting the dashboard data
        # `sections` defines which part of the data we want to include/exclude
        if sections is None:
            sections = self._get_dashboard_default_sections()
        result = {}
        if 'actions' in sections:
            # 'actions': -> Array of the different actions and their properties [
            #     {
            #         'string' -> Title for the line
            #         'count' -> Amount to display after the line
            #         'action' -> What to execute upon clicking the line
            #     }
            # ]
            # All actions can be either a xml_id or a dictionnary
            result['actions'] = self._get_dashboard_warnings_1()
        if 'batches' in sections:
            # Batches are loaded for the last 3 months with batches, for example if there are no batches for
            # the summer and september is loaded, we want to get september, june, may.
            # Limit to max - 1 year
            batch_limit_date = fields.Date.today() - relativedelta(years=1, day=1)
            batch_group_read = self.env['hr.payslip.run'].with_context(lang='en_US')._read_group(
                [('date_start', '>=', batch_limit_date)],
                fields=['date_start'],
                groupby=['date_start:month'],
                limit=20,
                orderby='date_start desc')
            # Keep only the last 3 months
            batch_group_read = batch_group_read[:3]
            if batch_group_read:
                if batch_group_read[-1]['__range'].get('date_start:month'):
                    min_date = datetime.strptime(batch_group_read[-1]['__range']['date_start:month']['from'],
                                                 '%Y-%m-%d')
                else:
                    min_date = fields.Date.today() - relativedelta(months=1, day=1)
                batches_read_result = self.env['hr.payslip.run'].search_read(
                    [('date_start', '>=', min_date)],
                    fields=self._get_dashboard_batch_fields())
            else:
                batches_read_result = []
            translated_states = dict(self.env['hr.payslip.run']._fields['state']._description_selection(self.env))
            for batch_read in batches_read_result:
                batch_read.update({
                    'name': f"{batch_read['name']} ({format_date(self.env, batch_read['date_start'], date_format='MM/y')})",
                    'payslip_count': _('(%s Payslips)', batch_read['payslip_count']),
                    'state': translated_states.get(batch_read['state'], _('Unknown State')),
                })
            result['batches'] = batches_read_result
        if 'notes' in sections:
            result['notes'] = {}
            # Fetch all the notes and their associated data
            dashboard_note_tag = self.env.ref('hr_payroll.payroll_note_tag', raise_if_not_found=False)
            if dashboard_note_tag:
                # For note creation
                result['notes'].update({
                    'tag_id': dashboard_note_tag.id,
                })
        if 'stats' in sections:
            result['stats'] = self._get_dashboard_stats()
        return result

    @api.model
    def _get_dashboard_warnings_1(self):
        # Retrieve the different warnings to display on the actions section (box on the left)
        result = []

        # Employees section
        employees_default_title = _('Employees')
        # Retrieve employees:
        # - with no open contract, and date_end in the past
        # - with no contract, and not green draft contract
        employees_without_contracts = self.env['hr.employee']
        all_employees = self.env['hr.employee'].search([
            ('employee_type', '=', 'employee'),
            ('company_id', 'in', self.env.companies.ids),
        ])
        today = fields.Date.today()
        for employee in all_employees:
            if employee.contract_id and employee.contract_id.date_end and employee.contract_id.date_end < today:
                employees_without_contracts += employee
            elif not employee.contract_id:
                existing_draft_contract = self.env['hr.contract'].search([
                    ('employee_id', '=', employee.id),
                    ('company_id', '=', employee.company_id.id),
                    ('state', '=', 'draft'),
                    ('kanban_state', '=', 'done'),
                ])
                if not existing_draft_contract:
                    employees_without_contracts += employee
        if employees_without_contracts:
            result.append({
                'string': _('موظفين بدون عقود'),
                'count': len(employees_without_contracts),
                'action': self._dashboard_default_action(employees_default_title, 'hr.employee',
                                                         employees_without_contracts.ids),
            })

        # Retrieve employees whose company on contract is different than employee's company
        employee_with_different_company_on_contract = self.env['hr.employee']
        contracts = self.sudo().env['hr.contract'].search([
            ('state', 'in', ['draft', 'open']),
            ('employee_id', 'in', all_employees.ids),
        ])

        for contract in contracts:
            if contract.employee_id.company_id != contract.company_id:
                employee_with_different_company_on_contract |= contract.employee_id
        if employee_with_different_company_on_contract:
            result.append({
                'string': _('الموظف الذي تختلف عقوده وشركته'),
                'count': len(employee_with_different_company_on_contract),
                'action': self._dashboard_default_action(employees_default_title, 'hr.employee',
                                                         employee_with_different_company_on_contract.ids),
            })

        # Retrieves last batches (this month, or last month)
        batch_limit_date = fields.Date.today() - relativedelta(months=1, day=1)
        batch_group_read = self.env['hr.payslip.run'].with_context(lang='en_US')._read_group(
            [('date_start', '>=', fields.Date.today() - relativedelta(months=1, day=1))],
            fields=['date_start'],
            groupby=['date_start:month'],
            orderby='date_start desc')
        # Keep only the last month
        batch_group_read = batch_group_read[:1]
        if batch_group_read:
            if batch_group_read[-1]['__range'].get('date_start:month'):
                min_date = datetime.strptime(batch_group_read[-1]['__range']['date_start:month']['from'], '%Y-%m-%d')
            else:
                min_date = batch_limit_date
            last_batches = self.env['hr.payslip.run'].search([('date_start', '>=', min_date)])
        else:
            last_batches = self.env['hr.payslip.run']

        payslips_with_negative_net = self.env['hr.payslip']

        employee_payslips = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))
        employee_calendar_contracts = defaultdict(lambda: defaultdict(lambda: self.env['hr.contract']))
        employee_payslip_contracts = defaultdict(lambda: self.env['hr.contract'])
        for slip in last_batches.slip_ids:
            if slip.state == 'cancel':
                continue
            employee = slip.employee_id
            contract = slip.contract_id
            calendar = contract.resource_calendar_id
            struct = slip.struct_id

            employee_payslips[struct][employee] |= slip

            employee_calendar_contracts[employee][calendar] |= contract

            employee_payslip_contracts[employee] |= contract

            if slip.net_wage < 0:
                payslips_with_negative_net |= slip

        employees_previous_contract = self.env['hr.employee']
        for employee, used_contracts in employee_payslip_contracts.items():
            if employee.contract_id not in used_contracts:
                employees_previous_contract |= employee

        employees_multiple_payslips = self.env['hr.payslip']
        for dummy, employee_slips in employee_payslips.items():
            for employee, payslips in employee_slips.items():
                if len(payslips) > 1:
                    employees_multiple_payslips |= payslips
        if employees_multiple_payslips:
            multiple_payslips_str = _('الموظفون الذين لديهم العديد من الكشوف المفتوحة من نفس النوع')
            result.append({
                'string': multiple_payslips_str,
                'count': len(employees_multiple_payslips.employee_id),
                'action': self._dashboard_default_action(multiple_payslips_str, 'hr.payslip',
                                                         employees_multiple_payslips.ids,
                                                         additional_context={'search_default_group_by_employee_id': 1}),
            })

        employees_missing_payslip = self.env['hr.employee'].search([
            ('company_id', 'in', last_batches.company_id.ids),
            ('id', 'not in', last_batches.slip_ids.employee_id.ids),
            ('contract_warning', '=', False)])
        if employees_missing_payslip:
            missing_payslips_str = _('الموظفون (بعقود سارية) مفقودون من الدُفعات المفتوحة')
            result.append({
                'string': missing_payslips_str,
                'count': len(employees_missing_payslip),
                'action': self._dashboard_default_action(missing_payslips_str, 'hr.contract',
                                                         employees_missing_payslip.contract_id.ids),
            })

        # Retrieve employees with both draft and running contracts
        ambiguous_domain = [
            ('company_id', 'in', self.env.companies.ids),
            ('employee_id', '!=', False),
            '|',
            '&',
            ('state', '=', 'draft'),
            ('kanban_state', '!=', 'done'),
            ('state', '=', 'open')]
        employee_contract_groups = self.env['hr.contract']._read_group(
            ambiguous_domain,
            fields=['state:count_distinct'], groupby=['employee_id'])
        ambiguous_employee_ids = [
            group['employee_id'][0] for group in employee_contract_groups if group['state'] == 2]
        if ambiguous_employee_ids:
            ambiguous_contracts_str = _('الموظفين مع كل من العقود الجديدة والجارية')
            ambiguous_contracts = self.env['hr.contract'].search(
                AND([ambiguous_domain, [('employee_id', 'in', ambiguous_employee_ids)]]))
            result.append({
                'string': ambiguous_contracts_str,
                'count': len(ambiguous_employee_ids),
                'action': self._dashboard_default_action(ambiguous_contracts_str, 'hr.contract',
                                                         ambiguous_contracts.ids,
                                                         additional_context={'search_default_group_by_employee': 1}),
            })

        # Work Entries section
        start_month = fields.Date.today().replace(day=1)
        next_month = start_month + relativedelta(months=1)
        work_entries_in_conflict = self.env['hr.work.entry'].search_count([
            ('state', '=', 'conflict'),
            ('date_stop', '>=', start_month),
            ('date_start', '<', next_month)])
        if work_entries_in_conflict:
            result.append({
                'string': _('تعارضات'),
                'count': work_entries_in_conflict,
                'action': 'hr_work_entry.hr_work_entry_action_conflict',
            })

        multiple_schedule_contracts = self.env['hr.contract']
        for employee, calendar_contracts in employee_calendar_contracts.items():
            if len(calendar_contracts) > 1:
                for dummy, contracts in calendar_contracts.items():
                    multiple_schedule_contracts |= contracts
        if multiple_schedule_contracts:
            schedule_change_str = _('Working Schedule Changes')
            result.append({
                'string': schedule_change_str,
                'count': len(multiple_schedule_contracts.employee_id),
                'action': self._dashboard_default_action(schedule_change_str, 'hr.contract',
                                                         multiple_schedule_contracts.ids,
                                                         additional_context={'search_default_group_by_employee': 1}),
            })

        # Nearly expired contracts
        date_today = fields.Date.from_string(fields.Date.today())
        outdated_days = fields.Date.to_string(date_today + relativedelta(days=+14))
        nearly_expired_contracts = self.env['hr.contract']._get_nearly_expired_contracts(outdated_days)
        if nearly_expired_contracts:
            result.append({
                'string': _('العقود الجارية تقترب من نهايتها'),
                'count': len(nearly_expired_contracts),
                'action': self._dashboard_default_action('Employees with running contracts coming to an end',
                                                         'hr.contract',
                                                         nearly_expired_contracts.ids)
            })

        # Payslip Section
        if employees_previous_contract:
            result.append({
                'string': _('تم إنشاء قسائم الدفع في العقد السابق'),
                'count': len(employees_previous_contract),
                'action': self._dashboard_default_action(
                    _('Employees with payslips generated on the previous contract'),
                    'hr.employee', employees_previous_contract.ids),
            })
        if payslips_with_negative_net:
            result.append({
                'string': _('كشوف الراتب بالمبالغ السالبة'),
                'count': len(payslips_with_negative_net),
                'action': self._dashboard_default_action(_('Payslips with negative NET'), 'hr.payslip',
                                                         payslips_with_negative_net.ids),
            })

        # new contracts warning
        new_contracts = self.env['hr.contract'].search([
            ('state', '=', 'draft'),
            ('employee_id', '!=', False),
            ('kanban_state', '=', 'normal')])
        if new_contracts:
            new_contracts_str = _('عقود جديدة')
            result.append({
                'string': new_contracts_str,
                'count': len(new_contracts),
                'action': self._dashboard_default_action(new_contracts_str, 'hr.contract', new_contracts.ids)
            })

        try:
            self.env['fleet.vehicle'].check_access_rights('read')
            self.env['fleet.vehicle.log.contract'].check_access_rights('read')
        except AccessError:
            return result

        self.env.cr.execute("""
                   SELECT v.id
                     FROM fleet_vehicle v
                    WHERE v.driver_employee_id IS NOT NULL
                      AND NOT EXISTS (SELECT 1
                                        FROM fleet_vehicle_log_contract c
                                       WHERE c.vehicle_id = v.id
                                         AND c.company_id = v.company_id
                                         AND c.active IS TRUE
                                         AND c.state = 'open')
                      AND v.company_id IN %s
                      AND v.active IS TRUE
                 GROUP BY v.id
               """, (tuple(self.env.companies.ids),))
        vehicles_no_contract = [vid[0] for vid in self.env.cr.fetchall()]

        if vehicles_no_contract:
            no_contract = _('المركبات بسائقين وبدون عقد')
            result.append({
                'string': no_contract,
                'count': len(vehicles_no_contract),
                'action': self._dashboard_default_action(no_contract, 'fleet.vehicle', vehicles_no_contract),
            })

        self.env.cr.execute("""
                   SELECT driver_employee_id
                     FROM fleet_vehicle
                    WHERE active IS TRUE
                      AND company_id IN %s
                 GROUP BY driver_employee_id
                   HAVING COUNT(driver_employee_id) > 1
               """, (tuple(self.env.companies.ids),))
        employees_multiple_vehicles = [eid[0] for eid in self.env.cr.fetchall()]

        if employees_multiple_vehicles:
            multiple_vehicles = _('الموظفين مع سيارات الشركة المتعددة')
            result.append({
                'string': multiple_vehicles,
                'count': len(employees_multiple_vehicles),
                'action': self._dashboard_default_action(multiple_vehicles, 'hr.employee', employees_multiple_vehicles),
            })

        leaves_to_defer = self.env['hr.leave'].search_read([
            ('payslip_state', '=', 'blocked'),
            ('state', '=', 'validate'),
        ], fields=['id'])
        if leaves_to_defer:
            result.append({
                'string': _('Time Off To Defer'),
                'count': len(leaves_to_defer),
                'action': 'hr_payroll_holidays.hr_leave_action_open_to_defer',
            })
        leaves_no_document = self.env['hr.leave'].search_read([
            ('state', 'not in', ['refuse', 'validate']),
            ('leave_type_support_document', '=', True),
            ('attachment_ids', '=', False)], fields=['id'])
        if leaves_no_document:
            no_document_str = _('إجازة بدون وثيقة الانضمام')
            result.append({
                'string': no_document_str,
                'count': len(leaves_no_document),
                'action': self._dashboard_default_action(no_document_str, 'hr.leave',
                                                         [l['id'] for l in leaves_no_document])
            })

        return result
