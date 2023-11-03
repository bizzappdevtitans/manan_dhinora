from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolStudent(TransactionCase):
    def setUp(self):
        super(TestSchoolStudent, self).setUp()
        self.student_record = self.env["school.student"].create(
            {
                "student_name": "Manan",
                "student_date_of_birth": date.today(),
            }
        )

        self.school_ref = self.env["school.reference"].create(
            {
                "reference_name": "ron",
                "reference_phone": "9968967890",
                "discount_amount": "30%",
            }
        )
        self.subject_record = self.env["school.subject"].create(
            {"subject_name": "hindi", "subject_credit": 6}
        )

    def test_01_duplicate(self):
        """checking if the inherited copy() method is working as intended #T00476"""
        self.student_record.copy()

    def test_02_reference_validation(self):
        """validating weather the promo_validation method works as intended #T00476"""
        self.student_record.write({"reference_code": self.school_ref.reference_promo})
        self.student_record.promo_validation()
        self.assertEqual(
            self.school_ref.reference_name,
            self.student_record.referral_name,
            "the refrence name logic not performing as expected",
        )

    def test_02_reference_validation_false(self):
        """testing to check weather the validation works as intended #T00476"""
        with self.assertRaises(ValidationError):
            self.student_record.write({"reference_code": "hi"})

    def test_03_unlink(self):
        """testing to check weather the inherited method unlink works as intended
        #T00476"""
        student_record_id = self.student_record.id
        with self.assertRaises(ValidationError):
            self.student_record.unlink()
        self.student_record.write({"deleteable": "Yes"})
        self.student_record.unlink()
        self.assertFalse(
            student_record_id in (self.env["school.student"].search([])).ids,
            "the record was not unlinked",
        )

    def test_04_compute_credit(self):
        self.student_record.write({"subject_ids": [(4, self.subject_record.id)]})
        self.assertTrue(
            self.student_record.total_subject_credit == 6,
            "the calculated credit doesn't match expected reasult",
        )

    def test_05_compute_grade(self):
        test_gpa = [1.0, 3.0, 5.0, 7.0, 9.0, 10.0]
        test_grade = ["F", "P", "B", "B+", "A", "A+"]

        for final_grade in zip(test_gpa, test_grade):
            gpa, grade = final_grade
            self.student_record.write({"student_gpa": gpa})
            self.assertEqual(
                self.student_record.student_grade,
                grade,
                "the grade obatined does not matched the expected grade",
            )
