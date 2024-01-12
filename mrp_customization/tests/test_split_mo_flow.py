from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSchoolRefernce(TransactionCase):
    def setUp(self):
        """New setup method to create products, bom and mo #T7141"""
        super(TestSchoolRefernce, self).setUp()
        self.product_1 = self.env["product.template"].create({"name": "product_1"})
        product = self.env["product.product"]
        self.product_2 = product.create({"name": "product_2"})
        self.product_3 = product.create({"name": "product_3"})

        self.bom_1 = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": self.product_1.id,
                "bom_line_ids": [
                    (0, 0, {"product_id": self.product_2.id, "product_qty": 1}),
                    (0, 0, {"product_id": self.product_3.id, "product_qty": 1}),
                ],
            }
        )
        self.mo = self.env["mrp.production"].create(
            {
                "product_id": self.product_1.product_variant_id.id,
                "bom_id": self.bom_1.id,
                "product_qty": 8.0,
            }
        )

    def test_01_mo_split(self):
        """New test case to test weather splitting of MO is working as intended
        #T7141"""
        self.bom_1.max_qty = 6.0
        with self.assertRaises(ValidationError):
            self.mo.split_mo_based_on_qty()
        self.bom_1.max_qty = 2.0
        self.mo.split_mo_based_on_qty()
        # checking weather the number of splitted MO is equal to the expected
        # amount #T7141
        self.assertEqual(
            self.mo.child_order_qty,
            self.env["mrp.production"].search_count([("parent_id", "=", self.mo.id)]),
            "The number of MO splits doesn't match the expected quantity",
        )
        self.assertTrue(self.mo.state == "cancle")
        self.mo.action_open_child_orders()
