# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SchoolEventsController(http.Controller):

    @http.route('/school/events/', auth='public', website=True, methods=['GET'])
    def list_school_events(self, **kwargs):
        # sudo() para que lo pueda ver cualquiera (si no, te puede bloquear por permisos)
        events = request.env['gestion_escolar.event'].sudo().search([])

        # Queremos enumerar los nombres generados por name_get()
        # name_get devuelve [(id, "Nombre personalizado"), ...]
        lines = []
        for _id, display in events.name_get():
            lines.append(f"- {display}")

        if not lines:
            lines = ["(No hay eventos)"]

        body = "EVENTOS DEL COLEGIO\n" + "\n".join(lines)

        # Devolvemos texto plano
        return request.make_response(
            body,
            headers=[('Content-Type', 'text/plain; charset=utf-8')]
        )
