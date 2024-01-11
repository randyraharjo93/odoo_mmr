# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Sale Account ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Account slice Sales based on MMR
    """,
    "depends": [
        'account',
        'mmr_sales_ext'
        ],
    'init_xml': [],
    'update_xml': [
        'data/mmr_account_data.xml',
        'views/account_views.xml',
        'views/sale_views.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
