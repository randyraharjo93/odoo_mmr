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
        'stock',
        'account',
        'mmr_description_UoM',
        ],
    'init_xml': [],
    'update_xml': [
        'data/mmr_sales_data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'report/report_deliveryslip.xml',
        'report/report_invoice.xml'
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
