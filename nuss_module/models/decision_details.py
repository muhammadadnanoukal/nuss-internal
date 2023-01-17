# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re
from werkzeug.urls import url_encode


class FormsModel(models.Model):
    _name = "decision.details"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="قرار رقم", readonly=True, default=lambda self: _('رقم'))
    date = fields.Date(string="التاريخ")
    decision_type = fields.Selection([
        ('type_1', 'قرارات جلسة'),
        ('type_2', 'قرارات لجنة رباعية'),
    ], required=True, string='النوع')

    details = fields.Many2one("work.schedule")

    type_of_decision = fields.Many2one("create.decisions.new")

    upload_file = fields.Many2one('decision.template')
    contents = fields.Html(related="upload_file.content", readonly=False)

    owner_of_the_relationship = fields.One2many('hr.employee', 'firstt', string='first')

    second = fields.One2many('res.partner', 'secondd', string='second')
    third = fields.One2many('res.partner', 'thirdd', string='third')
    forth = fields.One2many('res.partner', 'forthh', string='forth')
    fifth = fields.One2many('res.partner', 'fifthh', string='fifth')
    sixth = fields.One2many('res.partner', 'sixthh', string='sixth')
    seventh = fields.One2many('res.partner', 'seventhh', string='seventh')

    # owner_of_the_relationship = fields.One2many('res.partner', 'owner_of_relationship', string='owner of the relationship')

    sequence = fields.Integer(default=0)
    parent_form = fields.Many2one('work.schedule.stage')
    #
    #
    # list_partners =[[first],[second],[third],[forth],[fifth],[sixth],[seventh]]
    # # list_partners =[first,second,third,forth,fifth,sixth,seventh]
    # print(list_partners)
    #

    @api.onchange('decision_type')
    def decision_type_(self):
        return {'domain': {'upload_file': [('decision_type', '=', self.decision_type)]}}

    @api.model
    def create(self, vals):
        if vals.get('name', _('رقم')) == _('رقم'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kalb.kalb')
        result = super(FormsModel, self).create(vals)
        return result

    # @api.model
    # def create(self,vals):
    #     notifications_ids=[self.list_partners]
    #     print(notifications_ids)
    #     notifications_ids.appends((0, 0, {
    #         'res_partner_id': self.responsible_user_id.partner_id.id,
    #         'notification_type': 'inbox'
    #     }))
    #     self.env['mail.thread'].create(
    #         {
    #             'message_type': "notification",
    #             'body': "you have a notification for decision details" % self.name,
    #             'subject': "you have a notification for decision details" % self.name,
    #             'model': self._name,
    #             'res_id': self.id,
    #             'partner_ids': [
    #                 self.responsible_user_id.partner_id.id
    #             ],
    #             'author_id': self.env.user.partner_id.id,
    #             'notification_ids': self.notification_ids,
    #         }
    #     )

    # if users:
    #     notification_ids = [(0, 0,
    #                          {
    #                              'res_partner_id': user.partner_id.id,
    #                              'notification_type': 'inbox'
    #                          }
    #                          ) for user in users if users]
    # self.env['mail.message'].create({
    #     'message_type': "notification",
    #     'body': "Your Body",
    #     'subject': "Your Subject",
    #     'partner_ids': [(4, user.partner_id.id) for user in users if users],
    #     'model': self._name,
    #     'res_id': self.id,
    #     'notification_ids': notification_ids,
    #     'author_id': self.env.user.partner_id and self.env.user.partner_id.id
    # })

    #
    # def action_accept(self):
    #     display_msg = """Save"""
    #     self.message_post(body=display_msg)

    # def action_send(self):
    #     self.ensure_one()
    #     self.env['mail.thread'].message_notify(
    #         partner_ids=self.partner_id.ids,
    #         model_description='Referral Alerts',
    #         subject=self.subject,
    #         body=self.body,
    #         email_layout_xmlid='mail.mail_notification_light',
    #     )
    #     return True

    # @api.model
    # def create(self, values):
    #     all_users = self.env['res.partner'].search([('active', '=', True)])
    #
    #     my_users_group = all_users.filtered((lambda partner: partner.ids))
    #     for i in range(0, len(my_users_group)):
    #         item = my_users_group[i]
    #         item.message_post(body='New employee created', message_type='notification')
    #
    #     return super(FormsModel, self).create(values)

    # @api.multi
    # def make_pickings_auto_done(self):
    #
    #     emails = []
    #
    #     email_to = ''
    #
    #     mail_mail = self.env['mail.mail']
    #
    #     for pick in self:
    #         partner_ids = pick.message_follower_ids and pick.message_follower_ids.ids or []
    #
    #     for partner in self.env['mail.followers'].browse(partner_ids):
    #         emails.append(partner.partner_id.email)
    #
    #     product_dic = {}
    #
    #     for picking_line in pick.pack_operation_product_ids:
    #         product_dic.update({str(picking_line.product_id.name):
    #
    #                                 picking_line.qty_done})
    #
    #     for email in emails:
    #         email_to = email_to and email_to + ',' + email or email_to + email
    #
    #     do = pick.name and pick.name or ""
    #
    #     body_html = '''
    #
    #                                <div>
    #
    #                                   <p>
    #
    #                            Hello,
    #
    #                            <br/><br/>
    #
    #                                Delivery order ''' + do + ''' is move to done
    #
    #                                state.
    #
    #                                <br/><br/>
    #
    #                                The details of shipping is as below.
    #
    #                                <br/><br/>
    #
    #                            </p>
    #
    #                            <table border="1" cellpadding="5" cellspacing="1">
    #
    #                            <tbody>
    #
    #                                <tr>
    #
    #                                    <th>Delivery Order</th>
    #
    #                                    <th>Customer</th>
    #
    #                                    <th>Product</th>
    #
    #                                    <th>Qty</th>
    #
    #                                </tr>'''
    #
    #     for nm, qty in product_dic.iteritems():
    #         body_html += '''<tr>
    #
    #                                    <td>''' + do + '''</td>
    #
    #                                    <td>''' + pick.partner_id.name + '''</td>
    #
    #                                    <td>''' + nm + '''</td>
    #
    #                                    <td>''' + str(qty) + '''</td>
    #
    #                                </tr>'''
    #
    #     body_html += '''</tbody>
    #
    #                            </table>'''
    #
    #     mail_values = {
    #
    #         'email_from': self.company_id.partner_id.email or
    #
    #                       'noreply@localhost',
    #
    #         'email_to': email_to,
    #
    #         'subject': 'Delivery order ',
    #
    #         'body_html': body_html,
    #
    #         'state': 'outgoing',
    #
    #         'message_type': 'email',
    #
    #     }
    #
    #     mail_id = mail_mail.create(mail_values)
    #
    #     if mail_id:
    #
    #         for mail in mail_id:
    #             # To avoid sending mail/notification multiple times
    #
    #             return mail.send()
    #
    #     else:
    #
    #         return True