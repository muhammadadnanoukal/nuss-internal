# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SpecificOrders(models.Model):
    _name = "specific.orders"

    name = fields.Char(string='امر اداري')
    decision = fields.Many2one("administrative.orders",string="امر اداري")
