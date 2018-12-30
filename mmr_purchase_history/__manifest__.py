# -*- coding: utf-8 -*-
{
    'name' : 'Purhcase History on Purchase Form',
    'version' : '1.1',
    'summary': 'See history of purchase on purchases form',
    'sequence': 30,
    'author': ['Randy Raharjo'],
    'description': """
Module to help purchase. When they purchase something, they can see previous price directly on purchase form.
    """,
    'category': 'Purchases',
    'depends' : ['purchase'],
    'data': [
        'views/purchase_view.xml',
    ],
    'website': "randyraharjo@gmail.com",
    'installable': True,
    'application': False,
    'auto_install': False,
}
