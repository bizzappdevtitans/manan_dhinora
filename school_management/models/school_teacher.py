from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Tacher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "teacher_name"

    @api.model
    def default_get(self):
        """using system parameters to set default value for work_expreience #T00355"""
        field_list = []
        system_work_exp = self.env["ir.config_parameter"].get_param(
            "work_exprience", ""
        )
        default_values = super(SchoolTeacher, self).default_get(field_list)
        default_values["work_exprience"] = system_work_exp
        return default_values

    teacher_image = fields.Image(string="Image")
    teacher_name = fields.Char(string="Name", required=True)
    employee_email = fields.Char(string="Teacher Email", required=True)
    employee_number = fields.Char(string="Employee ID", default=lambda self: ("new"))
    teacher_gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender"
    )
    teacher_address = fields.Text(string="Address")
    date_of_birth_teacher = fields.Date(string="Date of Birth")
    work_exprience = fields.Float(string="Professional Exprience")
    teacher_zero_complain = fields.Boolean(string="Zero Complaint", default=True)
    teacher_salary_currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    teacher_salary = fields.Monetary(
        currency_field="teacher_salary_currency_id",
        compute="_compute_teacher_salary",
    )
    teacher_bonus = fields.Monetary(
        currency_field="teacher_salary_currency_id",
        compute="_compute_teacher_bonus",
    )
    student_ids = fields.One2many(
        comodel_name="school.student",
        inverse_name="class_teacher_id",
        string="studens",
    )
    # using this field for record rule implementation & smart button
    student_count = fields.Integer(compute="_compute_student_count", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirm"),
        ],
        default=lambda self: "draft",
    )
    joining_date = fields.Date(
        string="Date of Joining", default=lambda self: date.today()
    )
    days_from_joining = fields.Float(string="Days from joining")

    _sql_constraints = [
        ("unique_email", "UNIQUE(employee_email)", "This email is already used")
    ]

    @api.depends("work_exprience")
    def _compute_teacher_salary(self):
        """calculating the salary of teachers based on their work exprience #T00336"""
        self.teacher_salary = 10000
        if 0 < self.work_exprience < 3:
            self.teacher_salary = 15000
        elif 3 <= self.work_exprience < 5:
            self.teacher_salary = 20000
        elif 5 <= self.work_exprience < 7:
            self.teacher_salary = 40000
        elif 7 <= self.work_exprience:
            self.teacher_salary = 80000

    @api.depends("teacher_salary")
    def _compute_teacher_bonus(self):
        """using search_count() to find number of employees that are loyal based on this
        number we give out salaries #T00336"""
        zero_complain = self.search_count([("teacher_zero_complain", "=", True)])
        if 0 < zero_complain < 2:
            self.teacher_bonus = (self.teacher_salary * 10) / 100
        elif 2 <= zero_complain < 5:
            self.teacher_bonus = (self.teacher_salary * 15) / 100
        elif 5 <= zero_complain < 10:
            self.teacher_bonus = (self.teacher_salary * 25) / 100
        return self.teacher_bonus

    @api.depends("student_ids")
    def _compute_student_count(self):
        """getting the length i.e. number of records in the student_ids for
        the smart button #T00336"""
        self.student_count = len(self.student_ids)

    @api.ondelete(at_uninstall=True)
    def _ondelete_record(self):
        """implemented ondelete to make a record of past employees who will be deleted
        from school.teacher model #T00336"""
        return self.env["former.teachers"].create(
            {
                "former_teacher_image": self.teacher_image,
                "former_employee_number": self.employee_number,
                "former_teacher_name": self.teacher_name,
                "former_employee_email": self.employee_email,
                "former_teacher_address": self.teacher_address,
                "former_teacher_gender": self.teacher_gender,
                "former_teacher_zero_complain": self.teacher_zero_complain,
                "date_of_birth_former_teacher": self.date_of_birth_teacher,
                "former_teacher_work_exprience": self.teacher_salary,
                "former_teacher_salary": self.teacher_salary,
                "former_teacher_bonus": self.teacher_bonus,
            }
        )

    @api.model
    def create(self, vals):
        """we are inheriting teh create method to make an automated sequence"""
        if vals.get("employee_number", ("new")) == ("new"):
            vals["employee_number"] = self.env["ir.sequence"].next_by_code(
                "school.teacher"
            ) or ("new")
        final_sequence = super(SchoolTeacher, self).create(vals)
        return final_sequence

    @api.model
    def name_get(self):
        """using name_get() to get teacher name and email at the same time #T00336"""
        resultent_string = []
        for teacher in self:
            resultent_string.append(
                (teacher.id, "%s - %s" % (teacher.teacher_name, teacher.employee_email))
            )
        return resultent_string

    @api.model
    def name_search(self, name, args=None, limit=100, operator="ilike"):
        """using name_search() to search for both email and name of teachers #T00336"""
        args = args or []
        domain = self.search(
            ["|", ("teacher_name", operator, name), ("employee_email", operator, name)],
            limit=limit,
        )
        if not domain.ids:
            return super(SchoolTeacher, self).name_search(
                name=name, args=args, operator=operator, limit=limit
            )
        return domain.name_get()

    def wiz_teacher_leave(self):
        """wizard button to open the teacher leave wizard #T00345"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "teacher.leave.application.wizard",
            "view_mode": "form",
            "target": "new",
        }

    def action_student_count(self):
        """decleration of the Student smart button which shows number of students
        per teacher #T00336"""
        return {
            "name": ("Student"),
            "res_model": "school.student",
            "domain": [("class_teacher_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_validate(self):
        """python code to be executed when the server action is called #T00442"""
        active_record = self.env.context.get("active_id")
        active_record = self.search([("id", "=", active_record)])
        state = self.browse([active_record.id]).state
        date_of_birth = self.browse([active_record.id]).date_of_birth_teacher
        gender = self.browse([active_record.id]).teacher_gender
        if state == "confirm":
            raise ValidationError(_("Record is already confirmed"))
        elif date_of_birth and gender is False:
            raise ValidationError(_("please fill up all the details"))
        else:
            active_record.write({"state": "confirm"})

    def cron_day_counter(self):
        """python to be executed when the cron job runs #T00442"""
        record_set = self.search([])
        if record_set.ids:
            for record in record_set.ids:
                join_date = self.browse([record]).joining_date
                days = date.today() - join_date
                self.days_from_joining = days.total_seconds() / 86400
                return self.days_from_joining
