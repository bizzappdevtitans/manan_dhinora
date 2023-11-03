from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TeacherLeave(models.Model):
    _name = "teacher.leave"
    _description = "teacher leave wiz"
    _rec_name = "teacher_name"

    date_of_leave_start = fields.Date(string="Start Date", required=True)
    date_of_leave_end = fields.Date(string="End Date", required=True)
    total_leave_days = fields.Integer(store=True, compute="_compute_number_of_days")
    reason_for_leave = fields.Text(string="Reason", required=True)

    teacher_name = fields.Many2one(
        comodel_name="school.teacher", string="Name", required=True
    )
    currency_id_teacher_pay = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.user.company_id.currency_id.id,
    )
    pay_deduction = fields.Monetary(
        currency_field="currency_id_teacher_pay",
        string="Deduction",
        compute="_compute_pay_deduction",
    )

    @api.depends("total_leave_days")
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
        for deduction in self:
            if not deduction.total_leave_days - system_paid_leaves > 0:
                deduction.pay_deduction = 0
                return deduction.pay_deduction
            deduction.pay_deduction = (
                deduction.total_leave_days - system_paid_leaves
            ) * system_pay_per_day
        return deduction.pay_deduction

    @api.depends("date_of_leave_start", "date_of_leave_end")
    def _compute_number_of_days(self):
        today_date = date.today()
        if self.date_of_leave_start and self.date_of_leave_end:
            start_date = self.date_of_leave_start
            end_date = self.date_of_leave_end
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
        leaves = end_date - start_date
        # converted the above datetime.timedelta to an int
        leaves_sec = leaves.total_seconds() / 86400
        self.total_leave_days = int(leaves_sec)
        return self.total_leave_days
