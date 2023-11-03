from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolSubject(TransactionCase):
    def setUp(self):
        super(TestSchoolSubject, self).setUp()
        self.subject_record = self.env["school.subject"].create(
            {"subject_name": "hindi", "subject_credit": 6}
        )

    def test_01_credit_value_vaidation(self):
        with self.assertRaises(ValidationError):
            self.subject_record.write({"subject_credit": 2})

    def test_02_name_get(self):
        self.assertFalse(
            "hindi - 6" in self.subject_record.name_get(),
            "created name_get name is incorrect",
        )
