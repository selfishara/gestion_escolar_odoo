# -*- coding: utf-8 -*-
{
    'name': "academy",
    'summary': "Gestión de cursos y matrículas",
    'description': """
Módulo Academy: cursos, matrículas, vistas y endpoint público.
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Tools',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
    'installable': True,
}