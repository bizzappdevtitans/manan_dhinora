from odoo import fields, models


class FormerTeachers(models.Model):
    _name = "former.teachers"
    _description = "teachers that are no longer with the school"
    _rec_name = "former_teacher_name"

    # here all the fields are to be filled when a record is deleted form school.teacher
    # this model is only used in ondelete
    former_employee_number = fields.Char(string="former employee_number")
    former_teacher_image = fields.Image(
        string="Teacher Image",
    )
    former_teacher_name = fields.Char(
        string="Teacher Name",
        required=True,
    )
    former_employee_email = fields.Char(
        string="Teacher Email",
    )
    former_teacher_address = fields.Text(
        string="Teacher Address",
    )
    former_teacher_gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        string="Gender",
    )
    former_teacher_zero_complain = fields.Boolean(
        string="Zero Complaint",
    )
    date_of_birth_former_teacher = fields.Date(
        string="Teacher Birth Date",
    )
    former_teacher_work_exprience = fields.Float(
        string="Exprience",
    )
    former_teacher_salary_currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    former_teacher_salary = fields.Monetary(
        currency_field="former_teacher_salary_currency_id",
    )
    former_teacher_bonus = fields.Monetary(
        currency_field="former_teacher_salary_currency_id",
    )
