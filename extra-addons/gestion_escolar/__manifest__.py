# -*- coding: utf-8 -*-
{
    "name": "Gestión Escolar",
    "summary": "Gestión de alumnos, clases y eventos",
    "description": "Módulo para gestionar clases, alumnos y eventos.",
    "author": "Sara Martínez",
    "website": "https://www.yourcompany.com",
    "category": "Education",
    "version": "1.0",
    "application": True,
    "installable": True,
    "license": "LGPL-3",
    "depends": ["base", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
    ],
}
