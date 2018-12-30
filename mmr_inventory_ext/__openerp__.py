# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Inventory ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Inventory based on MMR
    """,
    "depends": [
        'base',
        'stock',
        ],
    'init_xml': [],
    'update_xml': [
        'views/stock_move_views.xml',
        'wizard/stock_report_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
