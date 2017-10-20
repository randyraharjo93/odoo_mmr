# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Description UoM",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add UoM just for description
    """,
    "depends": [
        'base',
        'stock',
        ],
    'init_xml': [],
    'update_xml': [
        'views/product_views.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
