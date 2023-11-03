from datetime import date, timedelta

from odoo import api, fields, models


class StudentFees(models.Model):
    _name = "student.fees"
    _description = "student fees"
    _rec_name = "fees_of_student_id"

    @api.model
    def default_get(self, field_list):
        """using get_default() to set a default fees amount"""
        today_date = date.today()
        system_set_fees = self.env["ir.config_parameter"].get_param(
            "school_management.student_fees"
        )
        system_deposite_date = self.env["ir.config_parameter"].get_param(
            "bank_deposite_date"
        )
        default_values = super(StudentFees, self).default_get(field_list)
        default_values["total_amount"] = system_set_fees
        final_bank_date = today_date + timedelta(days=int(system_deposite_date))
        default_values["date_of_bank_deposite"] = final_bank_date
        return default_values

    date_of_deposite = fields.Date(string="Date", required=True)
    date_of_bank_deposite = fields.Date(
        string="Bank deposite date",
        compute="_compute_bank_deposite_date",
    )
    fees_of_student_id = fields.Many2one(
        comodel_name="school.student", string="Name Of Student"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    total_amount = fields.Monetary(string="Amount", required=True)

    @api.depends("date_of_deposite")
    def _compute_bank_deposite_date(self):
        """changeing the bank deposite date based on value set in system
        parameters #T00355"""
        bank_deposite_parameter = self.env["ir.config_parameter"].get_param(
            "bank_deposite_date"
        )
        self.date_of_bank_deposite = self.date_of_deposite + timedelta(
            days=int(bank_deposite_parameter)
        )
        return self.date_of_bank_deposite
