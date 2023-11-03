from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolSubject(models.Model):
    _name = "school.subject"
    _description = "School Subject"
    _inherit = "res.config.settings"
    _rec_name = "subject_name"

    subject_name = fields.Char(string="Name", required=True)
    subject_credit = fields.Integer(required=True)
    subject_student_ids = fields.Many2many(
        comodel_name="school.student",
        relation="relation_table",
        column1="enroll_no",
        column2="subject",
    )

    @api.constrains("subject_credit")
    def validate_credit_value(self):
        """validating that the value of each subject is 30 >= >=5 #T00336 these credit
        values are going to be used in the implementation of ensure_one()"""
        if self.subject_credit > 30 or self.subject_credit < 5:
            raise ValidationError(
                _("credit value cannot be more than 30 or less than 5 per subject")
            )

    @api.constrains("subject_name")
    def excluded_subject_verification(self):
        """checking if the entred subject is the same as the one in
        system parameter #T00366"""
        system_set_subject_exclusion = self.env["ir.config_parameter"].get_param(
            "school_management.excluded_subject"
        )
        if system_set_subject_exclusion == self.subject_name:
            if system_set_subject_exclusion is not False:
                raise ValidationError(
                    _("invalid subject according to system parameters")
                )

    @api.model
    def name_get(self):
        """using name_get() to get subject_name and subject_credit #T00336"""
        resultent_string = []

        for subject in self:
            resultent_string.append(
                (subject.id, "%s - %s" % (subject.subject_name, subject.subject_credit))
            )
        return resultent_string
