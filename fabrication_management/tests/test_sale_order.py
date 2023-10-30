from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        sale_order = self.env["sale.order"]
        self.sale = sale_order.create(
            {
                "partner_id": self.env.ref("fabrication_management.res_partner_601").id,
                "maintenance_cycle": True,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref(
                                "fabrication_management.product_final_boiler"
                            ).product_variant_id.id,
                            "product_uom_qty": 1,
                            "welding_type": self.env.ref(
                                "fabrication_management.product_template_arc"
                            ).product_variant_id.id,
                        },
                    )
                ],
            }
        )

    def test_metal_used(self):
        self.assertEqual(
            self.sale.metal_used.id,
            self.env.ref("fabrication_management.product_steel_3").id,
            "Metal used not matched",
        )

    def test_action_confirm(self):
        pass
