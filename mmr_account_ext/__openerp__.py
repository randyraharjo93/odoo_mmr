# -*- coding: utf-8 -*-
# We have dependencies to odoo voip for now because alexandre want to hide this, but later we can remove it
{
    "name": "MMR Account ext",
    "version": "1.0",
    'author': 'Randy',
    "description": """
    Module to add additional functionality on Account based on MMR
    """,
    "depends": [
        'account',
        ],
    'init_xml': [],
    'update_xml': [
    ],
    'css': [],
    'js': [],
    'installable': True,
    'qweb': [
        ],
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
