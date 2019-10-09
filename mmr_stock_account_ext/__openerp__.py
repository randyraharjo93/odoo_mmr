# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Stock Account ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Stock Account based on Stupid Selfish Request
    """,
    "depends": [
        'stock_account', 'mmr_inventory_ext'
        ],
    'init_xml': [],
    'update_xml': [
        'wizard/change_date_wizard_views.xml',
        'wizard/wizard_valuation_history_views.xml',
        'views/stock_picking_views.xml',
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
