# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Deleted Record Check",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add Check if anyone delete a record
    """,
    "depends": [
        'base',
        'purchase',
        'sale',
        'account',
        'stock'
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
