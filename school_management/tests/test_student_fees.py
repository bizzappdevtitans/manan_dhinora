from datetime import date, timedelta

from odoo.tests.common import TransactionCase


class TestStudentFees(TransactionCase):
    def setUp(self):
        super(TestStudentFees, self).setUp()
        self.student_record = self.env["school.student"].create(
            {"student_name": "Manan", "student_date_of_birth": date.today()}
        )

        self.student_fees_record = self.env["student.fees"].create(
            {
                "fees_of_student_id": self.student_record.id,
                "date_of_deposite": date.today(),
                "total_amount": 500,
            }
        )

    def test_01_fees(self):
        """testing the deposite date compute field is working as intended #T00476"""
        self.assertEqual(
            self.student_fees_record.date_of_bank_deposite,
            date.today() + timedelta(days=2),
            "bank deposite date is not as expected",
        )
