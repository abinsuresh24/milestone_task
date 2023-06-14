# -*- coding: utf-8 -*-
{
    'name': "Milestone",
    'version': '16.0.1.0.0',
    'author': "Cybrosys_Technologies",
    'category': 'sales',
    'summary': 'Project milestone',
    'description': """
     Details of milestone in project
    """,
    'depends': ['base', 'mail', 'project', 'sale_management'],
    'data': [
        'views/sale_order_view.xml',
        'views/project_task_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'AGPL-3',
}
