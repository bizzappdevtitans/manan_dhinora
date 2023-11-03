from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestTeacherLeave(TransactionCase):
    def setUp(self):
        super(TestTeacherLeave, self).setUp()
        self.teacher_record_1 = self.env["school.teacher"].create(
            {
                "teacher_name": "Michael Scott",
                "employee_email": "michael.scott@dundermifflin.co.us",
            }
        )
        self.teacher_leave_request_1 = self.env["teacher.leave"].create(
            {
                "date_of_leave_start": date.today(),
                "date_of_leave_end": (date.today() + timedelta(days=7)),
                "reason_for_leave": "Testing this module",
                "teacher_name": self.teacher_record_1.id,
            }
        )

    def test_01_compute_total_leave(self):
        """verifing that the caculated total_leave_days is equal to the
        expected days #T00476"""
        self.assertEqual(
            self.teacher_leave_request_1.total_leave_days,
            7,
            "the total days compute is incorrect",
        )

    def test_02_compute_deduction(self):
        """verifing that the caculated pay_deduction is equal to
        the expected deduction #T00476"""
        paid_leaves = int(self.env["ir.config_parameter"].get_param("paid_leaves"))
        system_pay_per_day = int(
            self.env["ir.config_parameter"].get_param("pay_per_day")
        )
        deducted_pay = (
            self.teacher_leave_request_1.total_leave_days - paid_leaves
        ) * system_pay_per_day
        self.assertEqual(
            self.teacher_leave_request_1.pay_deduction,
            deducted_pay,
            "the total deducted pay is incorrect",
        )
