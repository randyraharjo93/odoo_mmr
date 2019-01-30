# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Purchase ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Purchase based on MMR
    """,
    "depends": [
        'base',
        'purchase',
        'account',
        'mmr_purchase_history'
        ],
    'init_xml': [],
    'update_xml': [
        'views/purchase_views.xml',
        'views/account_invoice_view.xml',
        'report/purchase_order_template.xml'
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
