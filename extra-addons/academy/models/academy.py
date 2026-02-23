# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AcademyCourse(models.Model):
    _name = 'academy.course'
    _description = 'Academy Course'

    name = fields.Char(required=True)
    duration = fields.Integer(string="Duration (hours)")
    category = fields.Selection(
        selection=[('online', 'Online'), ('presencial', 'Presencial')],
        string="Category"
    )
    max_students = fields.Integer(string="Max Students")

    enrollments = fields.One2many(
        comodel_name='academy.enrollment',
        inverse_name='course_id',
        string="Enrollments"
    )

    _sql_constraints = [
        ('course_name_unique', 'unique(name)', 'Course name must be unique.')
    ]

    # 3.1 Campo calculado (NO store)
    available_seats = fields.Integer(
        string="Available Seats",
        compute='_compute_available_seats',
        store=False
    )

    @api.depends('max_students', 'enrollments.state')
    def _compute_available_seats(self):
        for course in self:
            confirmed = len(course.enrollments.filtered(lambda e: e.state == 'confirmed'))
            course.available_seats = (course.max_students or 0) - confirmed


class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Academy Enrollment'
    _order = 'enrollment_date'

    student_name = fields.Char(required=True)
    enrollment_date = fields.Date(default=fields.Date.context_today)
    course_id = fields.Many2one('academy.course', string="Course", ondelete='cascade')

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='draft',
        required=True
    )

    # 3.2 name_get()
    def name_get(self):
        res = []
        for rec in self:
            course = rec.course_id.name or ""
            student = rec.student_name or ""
            res.append((rec.id, f"[{course}] - {student}"))
        return res