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
        self.student_record.copy()

    def test_02_reference_validation(self):

        self.student_record.write({"reference_code": self.school_ref.reference_promo})
        self.student_record.promo_validation()

    def test_02_reference_validation_false(self):
        with self.assertRaises(ValidationError):
            self.student_record.write({"reference_code": "hi"})

    def test_03_unlink(self):
        with self.assertRaises(ValidationError):
            self.student_record.unlink()
        self.student_record.write({"deleteable": "Yes"})
        self.student_record.unlink()

    def test_04_compute_credit(self):
        self.student_record.write({"subject_ids": [(4, self.subject_record.id)]})
