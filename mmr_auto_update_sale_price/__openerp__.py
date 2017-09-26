# -*- coding: utf-8 -*-
{
    "name": "MMR Auto Update Sale Price",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to give automatic new sale price based on latest purchase price
    """,
    "depends": [
        'sale',
        'purchase',
        ],
    'init_xml': [],
    'update_xml': [
        'wizard/price_update_notification_view.xml',
        'views/purchase_views.xml'
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
