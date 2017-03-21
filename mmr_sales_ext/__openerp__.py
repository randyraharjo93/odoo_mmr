# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Sales ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Sales based on MMR
    """,
    "depends": [
        'base',
        'sale',
        ],
    'init_xml': [],
    'update_xml': [
        'views/sale_order_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
