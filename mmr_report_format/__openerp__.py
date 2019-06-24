# -*- coding: utf-8 -*-
{
    "name": "MMR Report Format",
    "version": "1.0",
    'author': 'Randy',
    "description": """
        Report Format for MMR
    """,
    "depends": [
        'report',
        'mmr_sale_account_ext',
        'mmr_sale_inventory_ext'
        ],
    'init_xml': [],
    'update_xml': [
        'report/layout_templates.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
