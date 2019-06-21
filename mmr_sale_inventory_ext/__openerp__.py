# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Sales Inventory ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Inventory slice Sales based on MMR
    """,
    "depends": [
        'mmr_sales_ext',
        'mmr_inventory_ext',
        ],
    'init_xml': [],
    'update_xml': [
        'data/mmr_inventory_data.xml',
        'views/stock_move_views.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
