# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SchoolClass(models.Model):
    _name = "gestion_escolar.class"
    _description = "Clase"

    name = fields.Char(string="Nombre", required=True)

    grade = fields.Selection(
        selection=[
            ("first", "First"),
            ("second", "Second"),
            ("third", "Third"),
            ("fourth", "Fourth"),
        ],
        string="Curso",
    )

    date_begin = fields.Date(string="Fecha inicio")
    date_end = fields.Date(string="Fecha fin")

    tutor_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Tutor/a",
        ondelete="set null",
    )

    student_ids = fields.One2many(
        comodel_name="gestion_escolar.student",
        inverse_name="class_id",
        string="Alumnos",
    )

    student_number = fields.Integer(
        string="Número de alumnos",
        compute="_compute_student_number",
        store=True,
    )

    description = fields.Text(string="Descripción")

    @api.depends("student_ids")
    def _compute_student_number(self):
        for rec in self:
            rec.student_number = len(rec.student_ids)


class Student(models.Model):
    _name = "gestion_escolar.student"
    _description = "Alumno"

    name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellidos", required=True)

    id_number = fields.Char(string="DNI/NIE", required=True)

    birthdate = fields.Date(string="Fecha de nacimiento")
    active = fields.Boolean(string="Activo", default=True)

    age = fields.Integer(
        string="Edad",
        compute="_compute_age",
        store=True,
    )

    class_id = fields.Many2one(
        comodel_name="gestion_escolar.class",
        string="Clase",
        ondelete="set null",
    )

    event_ids = fields.Many2many(
        comodel_name="gestion_escolar.event",
        string="Eventos",
    )

    _sql_constraints = [
        ("id_number_unique", "unique(id_number)", "El DNI/NIE debe ser único."),
    ]

    @api.depends("birthdate")
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.birthdate:
                rec.age = today.year - rec.birthdate.year
            else:
                rec.age = 0


class SchoolEvent(models.Model):
    _name = "gestion_escolar.event"
    _description = "Evento"
    _order = "date asc"

    date = fields.Date(string="Fecha", required=True)

    type = fields.Selection(
        selection=[
            ("absence", "Absence"),
            ("delay", "Delay"),
            ("congratulations", "Congratulations"),
            ("behavior", "Behavior"),
        ],
        string="Tipo",
        required=True,
    )

    description = fields.Text(string="Descripción")

    student_ids = fields.Many2many(
        comodel_name="gestion_escolar.student",
        string="Alumnos",
    )

    def name_get(self):
        result = []
        type_label = dict(self._fields["type"].selection)

        for rec in self:
            tipo = type_label.get(rec.type, "Sin tipo")

            # Sacamos la clase a través de los alumnos vinculados
            clases = rec.student_ids.mapped("class_id.name")
            clase = clases[0] if clases else "Sin clase"

            display = f"{tipo} - {clase}"
            result.append((rec.id, display))

        return result
