# -*- coding: utf-8 -*-
{
    'name' : 'Partner Group',
    'version' : '1.1',
    'summary': 'Add function to give group to partner.',
    'author': ['Randy Raharjo'],
    'sequence': 30,
    'description': """
Module to add function : Grouping partner.
    """,
    'category': 'Tools',
    'depends' : ['contacts'],
    'data': [
        'views/res_partner_view.xml',
        'security/ir.model.access.csv'
    ],
    'website': "randyraharjo@gmail.com",
    'installable': True,
    'application': False,
    'auto_install': False,
}
