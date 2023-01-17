# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Proofs(models.Model):
    _inherit = ["hr.employee"]

    custom_address_home = fields.Many2one(related='address_home_id', groups="base.group_user")
    one = fields.Many2one("documents.document", string="لا حكم عليه",
                          domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    two = fields.Many2one("documents.document", string="بيان تجنيد",
                          domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    three = fields.Many2one("documents.document", string="استمارة التأمينات رقم 1",
                            domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    four = fields.Many2one("documents.document", string="استمارة التأمينات رقم 2",
                           domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    five = fields.Many2one("documents.document", string="قرارات",
                           domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    six = fields.Many2one("documents.document", string="صورة شخصية",
                          domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    seven = fields.Many2one("documents.document", string="صورة هوية",
                            domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    eight = fields.Many2one("documents.document", string="دفتر عائلة",
                            domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    nieght = fields.Many2one("documents.document", string="بيان عائلي",
                             domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")
    ten = fields.Many2one("documents.document", string="شهادات تعليمية",
                          domain="['|', ('partner_id', '=', custom_address_home), ('owner_id', '=', user_id)]")

    # def read(self, fields=None, load='_classic_read'):
    #
    #     return records
    # def set_domain_for_document(self):
    #     res = {}
    #     res['domain'] = {'one': ['|',('partner_id', '=', self.address_home_id.id),
    #                              ('owner_id', '=', self.user_id.id)]}
    #     return res







