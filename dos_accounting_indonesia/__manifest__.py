# -*- coding: utf-8 -*-
{
    "name": "Accounting Indonesia",
    "version": "1.0",
    'author': 'Databit Solusi Indonesia',
    "description": """
    Change view for Indonesia
    """,
    "depends": ['account', 'dos_amount_to_text_id'],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'views/faktur_pajak.xml',
        'views/invoice_inherit_view.xml',
        'wizard/generate_faktur_view.xml',
    ],
    'css': [],
    'js': [
    ],
    'installable': True,
    'active': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
