from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestLeaveWizard(TransactionCase):
    def setUp(self):
        super(TestLeaveWizard, self).setUp()

        self.leave_wiz_record = self.env["teacher.leave.application.wizard"].create(
            {
                "date_of_leave_start_wizard": date.today(),
                "date_of_leave_end_wizard": (date.today() + timedelta(days=7)),
                "reason_for_leave_wizard": "KHello",
            }
        )

    def test_01_check_total_leave_days(self):
        """verifing that the caculated total_leave_days is equal to the
        expected days #T00476"""
        self.assertEqual(
            self.leave_wiz_record.total_leave_days_wizard,
            7,
            "the computed leave days is not equal to the expected value",
        )

    def test_02_compute_pay_deduction(self):
        """verifing that the caculated pay_deduction_wizard is equal to
        the expected deduction #T00476"""
        paid_leaves = int(self.env["ir.config_parameter"].get_param("paid_leaves"))
        system_pay_per_day = int(
            self.env["ir.config_parameter"].get_param("pay_per_day")
        )
        deducted_pay = (
            self.leave_wiz_record.total_leave_days_wizard - paid_leaves
        ) * system_pay_per_day
        self.assertEqual(
            self.leave_wiz_record.pay_deduction_wizard,
            deducted_pay,
            "the total deducted pay is incorrect in wizard",
        )
