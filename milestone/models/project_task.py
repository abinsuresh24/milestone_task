# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTask(models.Model):
    """This model is for inheriting project task
    and adding a field order line number"""
    _inherit = 'project.task'

    order_lines_number = fields.Integer(string='Order id')
