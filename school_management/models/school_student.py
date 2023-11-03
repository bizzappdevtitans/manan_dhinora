import re
from datetime import date, datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "student_name"

    student_image = fields.Image(string="Image")
    enroll_no = fields.Char(
        string="enroll",
        index=True,
        default=lambda self: ("new"),
        copy=False,
    )
    student_name = fields.Char(string="Name", required=True)
    student_surname = fields.Char(string="surname")
    student_gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender"
    )
    student_address = fields.Text(string="Address", tracking=True)
    student_date_of_birth = fields.Date(string="Date of Birth", required=True)
    student_age = fields.Integer(
        string="Age", compute="_compute_student_age", store=True, default=0
    )
    calendar_birth_day = fields.Date(compute="_compute_birth_date", store=True)
    student_name_birthday = fields.Char(
        string="Birthday", compute="_compute_birthday_name"
    )
    student_gpa = fields.Float(digits=(2, 2), tracking=True)
    student_grade = fields.Char(tracking=True)
    class_teacher_id = fields.Many2one(
        comodel_name="school.teacher", string="Class Teacher"
    )
    reference_code = fields.Char(string="Promo Code")
    referral_name = fields.Char(
        store=True,
    )
    subject_ids = fields.Many2many(
        comodel_name="school.subject",
        relation="relation_table",
        column1="subject",
        column2="enroll_no",
    )
    payment_count = fields.Char(compute="_compute_amount_payment")
    fees_table_ids = fields.One2many(
        comodel_name="student.fees",
        inverse_name="fees_of_student_id",
    )
    deleteable = fields.Selection([("Yes", "yes"), ("No", "no")])
    total_subject_credit = fields.Integer(
        compute="_compute_total_subject_credit",
        store=True,
    )
    # using this field to implement ensure_one()
    more_than_one = fields.Boolean(string="only one subject")

    @api.depends("subject_ids")
    def _compute_total_subject_credit(self):
        """using ensure_one() to check if the input record is only one and then
        calculating the total credit based on number of inputs #T00336"""
        iterable_subjects = self.subject_ids.ids
        final_list = []
        # checking if the subject_ids field is empty or not
        if not iterable_subjects:
            self.total_subject_credit = 0
            return self.total_subject_credit

        # checking if the more_than_one field is true or false
        if not self.more_than_one:
            for rec in iterable_subjects:
                credit_values = self.env["school.subject"].browse(rec).subject_credit
                final_list.append(credit_values)
            total_credit = sum(final_list)
            self.total_subject_credit = total_credit
            return self.total_subject_credit
        # if the boolean is set to true
        self.subject_ids.ensure_one()
        # we ensure_one() as .browse only takes one record at a time
        credit_values = (
            self.env["school.subject"].browse(self.subject_ids.ids).subject_credit
        )
        self.total_subject_credit = credit_values
        return self.total_subject_credit

    @api.depends("fees_table_ids")
    def _compute_amount_payment(self):
        """counting the number of fees depoistes made by the student for
        the smart button #T00336"""
        self.payment_count = len(self.fees_table_ids)

    @api.depends("student_date_of_birth")
    def _compute_student_age(self):
        """calculating age based on the input birth year #T00336"""
        self.student_age = datetime.today().year - self.student_date_of_birth.year
        return self.student_age

    @api.onchange("student_gpa")
    def _onchange_gpa_calculate_grade(self):
        """using onchange to check for gradeof student based on gpa #T00336"""
        if self.student_gpa > 9.00:
            self.student_grade = "A+"
        elif 9.00 >= self.student_gpa > 8.00:
            self.student_grade = "A"
        elif 8.00 >= self.student_gpa > 6.00:
            self.student_grade = "B+"
        elif 6.00 >= self.student_gpa > 4.00:
            self.student_grade = "B"
        elif 4.00 >= self.student_gpa > 2.00:
            self.student_grade = "P"
        elif 2.00 >= self.student_gpa >= 0.00:
            self.student_grade = "F"

    @api.depends("student_date_of_birth")
    def _compute_birth_date(self):
        """computing the birthday of the student for the current year to show
        it in the calendar view #T00336"""
        if self.student_date_of_birth:
            # here the birth date provided is being converted to current year
            day_month = str(
                str(self.student_date_of_birth.day)
                + "/"
                + str(self.student_date_of_birth.month)
                + "/"
                + str(date.today().year)
            )
            # now we convert the current birth date back to datetime format
            self.calendar_birth_day = datetime.strptime(day_month, "%d/%m/%Y")
            return self.calendar_birth_day

    @api.depends("student_name")
    def _compute_birthday_name(self):
        """here we are showing the name of the student whose birthday it is in
        the calendar view event #T00336"""
        self.student_name_birthday = self.name + " " + self.student_surname
        return self.student_name_birthday

    @api.constrains("reference_code")
    def promo_validation(self):
        """using search() and browse() to verify the referal code #T00336"""
        if self.reference_code is not False:
            reffral_name_ids = (
                self.env["school.reference"]
                .search([("reference_promo", "=", self.reference_code)])
                .ids
            )
            if reffral_name_ids:
                for element in reffral_name_ids:
                    required_element = int(element)
                    # using browse to get the referral's name
                    reffral_name_browse = (
                        self.env["school.reference"]
                        .browse([required_element])
                        .reference_name
                    )
                    self.referral_name = reffral_name_browse
                    return self.referral_name
            raise ValidationError(_("invalid code"))

    # validating that the input name doesn't have numbers
    @api.constrains("student_name")
    def validate_student_name(self):
        """checking if the name field is empty as "open wizard" button won't work
        if the field is empty. Using re to validate the name has no numbers
        in it #T00336"""
        if not self.student_name:
            raise ValidationError(_("please enter a name to continue"))
        excluded_char = re.findall(r"[0-9]+", self.student_name)
        #   if bool(excluded_char) is True:
        if excluded_char:
            raise ValidationError(_("Numbers not allowed in name"))

    @api.model
    def create(self, vals):
        """here checking if the field says 'new'
        if yes we give it an automated squence number but if its says copy new we give
        it another sequence specially made for copied records #T00336"""
        if vals.get("enroll_no", ("new")) == ("new"):
            vals["enroll_no"] = self.env["ir.sequence"].next_by_code("school.student")
        elif vals.get("enroll_no", ("copy new")) == ("copy new"):
            vals["enroll_no"] = self.env["ir.sequence"].next_by_code(
                "copy.school.student"
            ) or ("copy new")
        return super(SchoolStudent, self).create(vals)

    def copy(self, default=None):
        """when a record is copied its enroll_no field will be changed to copy new
        which will furhter be replaced by an automated squence used for copied records
        only using create ORM method. #T00336"""
        if default is None:
            default = {}
        if not default.get("enroll_no"):
            default["enroll_no"] = "copy new"
        return super(SchoolStudent, self).copy(default)

    def unlink(self):
        """inheriting unlink method and checking if the deleteable field is set to
        yes or not #T00336"""
        if self.deleteable != "Yes":
            raise ValidationError(_("can't delete as 'delete ?' is set to No"))
        return super(SchoolStudent, self).unlink()

    def action_payment_count(self):
        """defining a smart button to show the number of deposited found
        in above functions #T00336"""
        return {
            "name": "Payments",
            "res_model": "student.fees",
            "domain": [("fees_of_student_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
            "type": "ir.actions.act_window",
        }
