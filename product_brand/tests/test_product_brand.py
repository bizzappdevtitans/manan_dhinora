from odoo.tests.common import TransactionCase


class TestProductBrand(TransactionCase):
    def setUp(self):
        """Inherited Setup method to create new products, product_brand, res_partner,
        invoice #T7127"""
        super(TestProductBrand, self).setUp()
        self.product_1 = self.env["product.product"].create({"name": "test_product_1"})
        self.product_2 = self.env["product.product"].create({"name": "test_product_2"})
        self.product_brand_1 = self.env["product.brand"].create(
            {"name": "test_brand_1"}
        )
        self.product_brand_2 = self.env["product.brand"].create(
            {"name": "test_brand_2"}
        )
        self.res_partner = self.env["res.partner"].create({"name": "Jindal partner"})
        self.account_move = self.env["account.move"].create(
            {"partner_id": self.res_partner.id}
        )

    def test_product_brand(self):
        """New method to test if the product_brand_id field and product_ids fields are
        working as intended and are updating if one is changed #T7127"""
        self.product_brand_1.write({"product_ids": [(4, self.product_1.id)]})
        self.assertEqual(
            self.product_brand_1.id,
            self.product_1.product_brand_id.id,
            """product_brand_id not in product_ids at product_brand,
             when set from product_brand_id""",
        )
        self.product_2.write({"product_brand_id": self.product_brand_2.id})
        self.assertTrue(
            self.product_2.id in self.product_brand_2.product_ids.ids,
            """product_brand_id not in product_ids at product_brand,
             when set from product_product""",
        )
