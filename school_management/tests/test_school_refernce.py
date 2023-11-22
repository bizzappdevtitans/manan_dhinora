from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolRefernce(TransactionCase):
    def setUp(self):
        super(TestSchoolRefernce, self).setUp()
        self.school_ref = self.env["school.reference"].create(
            {
                "reference_name": "ron",
                "reference_phone": "9968967890",
                "discount_amount": "30%",
            }
        )

    def test_01_promo_generator(self):
        """testing for is the name validation works #T00476"""
        self.assertEqual(
            len(self.school_ref.reference_promo),
            13,
            "the generated code is not at expected length",
        )
        invalid_data = {
            "reference_name": "ron1",
            "reference_phone": "9968967890",
            "discount_amount": "30%",
        }
        # checking if a validation error is raised if we input invalid data
        with self.assertRaises(ValidationError):
            self.env["school.reference"].create(invalid_data)
