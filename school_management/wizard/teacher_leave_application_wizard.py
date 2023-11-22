from datetime import date, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TeacherLeaveApplicationWizard(models.TransientModel):
    _name = "teacher.leave.application.wizard"
    _description = "wizard for teacher leave"

    @api.model
    def default_get(self, field_list):
        today_date = date.today()
        parameter_time_delta = self.env["ir.config_parameter"].get_param("date_offest")
        default_values = super(TeacherLeaveApplicationWizard, self).default_get(
            field_list
        )
        final_default_date = today_date + timedelta(days=int(parameter_time_delta))
        default_values["date_of_leave_start_wizard"] = final_default_date
        return default_values

    # input fields for the wizard
    date_of_leave_start_wizard = fields.Date(string="start date", required=True)
    date_of_leave_end_wizard = fields.Date(string="end date", required=True)
    reason_for_leave_wizard = fields.Text(string="Reason", required=True)
    total_leave_days_wizard = fields.Integer(compute="_compute_number_of_days")
    currency_id_teacher_pay = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    pay_deduction_wizard = fields.Monetary(
        currency_field="currency_id_teacher_pay",
        string="Deduction",
        compute="_compute_pay_deduction",
    )

    @api.depends("date_of_leave_start_wizard", "date_of_leave_end_wizard")
    def _compute_number_of_days(self):
        """computing the number of net days of leave that is applied #T00355"""
        today_date = date.today()
        if self.date_of_leave_start_wizard and self.date_of_leave_end_wizard:
            start_date = self.date_of_leave_start_wizard
            end_date = self.date_of_leave_end_wizard
        else:
            start_date = today_date
            end_date = today_date
        # validating the input dates
        if start_date < today_date:
            raise ValidationError(_("invalid start date"))
        elif end_date < start_date:
            raise ValidationError(_("invalid end date"))
        elif end_date < today_date:
            raise ValidationError(_("invalid end date"))
        # calculating the number of days of leaves
        leaves = (end_date - start_date).total_seconds() / 86400
        # converted the above datetime.timedelta to an int
        self.total_leave_days_wizard = int(leaves)
        return self.total_leave_days_wizard

    @api.depends("total_leave_days_wizard")
    def _compute_pay_deduction(self):
        """here using system parameters to set the value for paid leaves
        and pay/day #T00355"""
        system_paid_leaves = int(
            self.env["ir.config_parameter"].get_param("paid_leaves")
        )
        system_pay_per_day = int(
            self.env["ir.config_parameter"].get_param("pay_per_day")
        )
        # calculating deducted pay, if any
        if not self.total_leave_days_wizard - system_paid_leaves > 0:
            self.pay_deduction_wizard = 0
            return self.pay_deduction_wizard
        self.pay_deduction_wizard = (
            self.total_leave_days_wizard - system_paid_leaves
        ) * system_pay_per_day
        return self.pay_deduction_wizard

    def create_record_teacher_leave(self):
        """function to input data into the teacher leave model i.e. connection transient
        model the a regular model #T00354"""
        return self.env["teacher.leave"].create(
            {
                "teacher_name": self.env.context.get("active_id"),
                "date_of_leave_start": self.date_of_leave_start_wizard,
                "date_of_leave_end": self.date_of_leave_end_wizard,
                "reason_for_leave": self.reason_for_leave_wizard,
                "total_leave_days": self.total_leave_days_wizard,
                "pay_deduction": self.pay_deduction_wizard,
            }
        )
