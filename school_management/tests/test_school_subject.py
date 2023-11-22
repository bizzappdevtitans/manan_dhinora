from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolSubject(TransactionCase):
    def setUp(self):
        super(TestSchoolSubject, self).setUp()
        self.subject_record = self.env["school.subject"].create(
            {"subject_name": "hindi", "subject_credit": 6}
        )

    def test_01_credit_value_vaidation(self):
        """testing for the validation error, if credit < 5 #T0476"""
        with self.assertRaises(ValidationError):
            self.subject_record.write({"subject_credit": 2})

    def test_02_name_get(self):
        """testing that the name found after running name_get is as expected #T00476"""
        self.assertFalse(
            "hindi - 6" in self.subject_record.name_get(),
            "name_get return value does not match the expected value",
        )
