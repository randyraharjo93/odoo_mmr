# -*- coding: utf-8 -*-
{
    'name' : 'Sale History on Sales Form',
    'version' : '1.1',
    'summary': 'See history of sales on sales form',
    'sequence': 30,
    'author': ['Randy Raharjo'],
    'description': """
Module to help sales. When they sale something, they can see previous price directly on sales form.
    """,
    'category': 'Sales',
    'depends' : ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'website': "randyraharjo@gmail.com",
    'installable': True,
    'application': False,
    'auto_install': False,
}
