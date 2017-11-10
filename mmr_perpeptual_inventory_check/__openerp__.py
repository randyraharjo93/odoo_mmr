# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Perpeptual Inventory Check",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add help checking on inventory Perpetual
    """,
    "depends": [
        'base',
        'stock',
        'account'
        ],
    'init_xml': [],
    'update_xml': [
        'report/perpeptual_inventory_check_pdf.xml',
        'wizard/perpeptual_inventory_check_reports.xml'
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
