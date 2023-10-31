from datetime import date

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
        """testing a compute field 'metal_used' as the input field is know we
        can check the output using static value #T00469"""
        self.assertEqual(
            self.sale.metal_used.id,
            self.env.ref("fabrication_management.product_steel_3").id,
            "Metal used not matched",
        )

    def test_action_confirm(self):
        """testing the inherited method '_action_confirm' as it is used to create
        project & task when sale order is confirmed #T00469"""
        self.sale._action_confirm()
        created_project = self.env["project.project"].search(
            [("sale_order_ref", "=", self.sale.id)]
        )
        created_project_name = str(created_project.mapped("name")) + str(date.today())
        self.assertEqual(created_project_name, created_project.name, "incorrect name")
        order_line_ids = self.sale.orderline.ids
        self.assertEqual(
            len(order_line_ids),
            self.sale.task_length,
            "Task created not equal to the expected amount",
        )
