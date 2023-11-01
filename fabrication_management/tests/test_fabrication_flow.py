from odoo.tests.common import TransactionCase


class TestFabricationFlow(TransactionCase):
    def setUp(self):
        super(TestFabricationFlow, self).setUp()
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

    def test_01_metal_used(self):
        """testing a compute field 'metal_used' as the input field is know we
        can check the output using static value #T00469"""
        self.assertEqual(
            self.sale.metal_used.id,
            self.env.ref("fabrication_management.product_steel_3").id,
            "Metal used not matched",
        )

    def test_02_sale_action_confirm(self):
        """testing the inherited method '_action_confirm' as it is used to create
        project & task when sale order is confirmed #T00469"""
        self.sale.action_confirm()
        created_project = self.env["project.project"].search(
            [("sale_order_ref", "=", self.sale.id)]
        )
        created_project_name = (
            str((self.sale.partner_id.mapped("name"))[0])
            + " - "
            + str(self.sale.date_order)
        )
        self.assertEqual(created_project_name, created_project.name, "incorrect name")
        order_line_ids = self.sale.order_line.ids
        self.assertEqual(
            len(order_line_ids),
            self.sale.task_length,
            "Task created not equal to the expected amount",
        )

    def test_03_sale_smart_buttons_to_project_task(self):
        """testing the smart button to project and task which appear after creating
        a sale order #T00469"""
        self.sale.action_confirm()
        if self.sale.state == "sale":
            self.sale.action_project_view()
            self.sale.action_task_view()

    def test_04_replenish_cron(self):
        """testing for the cron job which replineshes welding materials #T00469"""
        self.sale._replenish_welding_materials_cron()
        self.assertTrue(
            self.env["purchase.order"].search(
                [("description", "=", "created due to replenishment")]
            ),
            "a purchase order was not created, when replineshment cron ran",
        )

    def test_05_purchase_smart_button(self):
        """testing that the button on purchase order created from mrp will have to
        smart button to the correct sale order #T00469"""
        purchase = self.env["purchase.order"]
        self.sale.action_confirm()
        created_po = purchase.search([("sale_ref_id", "=", self.sale.id)]).ids
        po_res_id = set()
        for po in created_po:
            so_id = purchase.browse([po]).action_sale_mrp_reference().get("res_id")
            po_res_id.add(so_id)
        self.assertEqual(
            list(po_res_id)[0],
            self.sale.id,
            "smart button on purchase returns wront sale order",
        )
