# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Customer Visit Management",
    "version": "1.0",
    'author': 'Randy',
    "description": """
        Add Customer Visit module
    """,
    "depends": [
        'sale',
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'security/visit_security.xml',
        'views/mmr_visit_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
