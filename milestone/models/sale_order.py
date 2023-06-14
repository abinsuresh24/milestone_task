# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    """class defined for adding commission in the sales sale order"""
    _inherit = 'sale.order'

    task_count = fields.Integer(string='Task count', default=0)

    def action_create_project(self):
        """Function defined for creating project and task from sale order"""
        self.task_count = 1
        project = self.env['project.project'].create({
            'name': self.name,
            'partner_id': self.partner_id.id
        })
        for line in self.order_line:
            if line.milestone:
                task_name = 'Milestone' + ' ' + str(line.milestone)
                existing_task = self.env['project.task'].search(
                    [('name', '=', task_name), ('project_id', '=', project.id)])
                if existing_task:
                    existing_task.create({
                        'name': line.product_template_id.name,
                        'parent_id': existing_task.id,
                        'order_lines_number': line.id
                    })
                else:
                    task = self.env['project.task'].create({
                        'name': task_name,
                        'project_id': project.id,
                    })
                    self.env['project.task'].create({
                        'name': line.product_template_id.name,
                        'parent_id': task.id,
                        'order_lines_number': line.id
                    })

    def smart_button_project(self):
        """Function defined for smart button to show project"""
        tasks = self.env['project.project'].search(
            [('name', '=', self.name)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'milestone',
            'view_mode': 'kanban,form',
            'res_model': 'project.project',
            'domain': [('id', '=', tasks.id)],
            'context': {'create': False}
        }

    def action_update_project(self):
        """Function defined for update project if new order line is
        added in the sale order"""
        project = self.env['project.project'].search(
            [('name', '=', self.name)])
        for line in self.order_line:
            if line.milestone:
                task_name = 'Milestone' + ' ' + str(line.milestone)
                subtask_name = line.product_template_id.name
                existing_task = self.env['project.task'].search([
                    ('name', '=', task_name),
                    ('project_id', '=', project.id)], limit=1)
                if existing_task:
                    existing_subtask_ids = self.env['project.task'].search([
                        ('order_lines_number', '=', line.id),
                        ('parent_id', '=', existing_task.id),
                    ])
                    if not existing_subtask_ids:
                        self.env['project.task'].create({
                            'name': subtask_name,
                            'project_id': project.id,
                            'parent_id': existing_task.id,
                            'order_lines_number': line.id
                        })
                else:
                    new_task = self.env['project.task'].create({
                        'name': task_name,
                        'project_id': project.id,
                        'milestone_id': line.milestone
                    })
                    self.env['project.task'].create({
                        'name': subtask_name,
                        'project_id': project.id,
                        'parent_id': new_task.id,
                        'order_lines_number': line.id
                    })


class SaleOrderLine(models.Model):
    """class defined for adding milestone in the sale order"""
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string="Milestone")
