# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class AcademyController(http.Controller):

    @http.route('/academy/courses', auth='public', methods=['GET'], csrf=False)
    def academy_courses(self, **kw):
        courses = request.env['academy.course'].sudo().search([])
        lines = [name for (_id, name) in courses.name_get()]
        return "\n".join(lines)