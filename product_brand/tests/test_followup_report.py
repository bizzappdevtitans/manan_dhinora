from freezegun import freeze_time

from odoo import Command
from odoo.tests import tagged

from odoo.addons.account_reports.tests.common import TestAccountReportsCommon


@tagged("post_install", "-at_install")
class TestAccountFollowupReports(TestAccountReportsCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        """Inherited setup method from TestAccountReportsCommon to write test for
        follow-up report #T7127"""
        super().setUpClass(chart_template_ref=chart_template_ref)
        # adding more data for the fields that are going to be used in below testcase
        # #T7127
        cls.partner_a.email = "partner_a@mypartners.xyz"
        cls.product_brand = cls.env["product.brand"].create({"name": "Brand_a"})
        cls.product_1 = cls.env["product.product"].create(
            {"name": "product_1", "product_brand_id": cls.product_brand.id}
        )

    def test_01_followup_report(self):
        """New method to test report line values from the dict that creates the
        follow-up report #T7127"""
        report = self.env["account.followup.report"]
        options = {
            "partner_id": self.partner_a.id,
        }
        # creating and confirming a new invoice to then create a follow-up report on
        # that invoice #T7127
        invoice_1 = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "invoice_date": "2016-01-01",
                "partner_id": self.partner_a.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "quantity": 1,
                            "price_unit": 500,
                            "tax_ids": [],
                        }
                    )
                ],
            }
        )
        invoice_1.action_post()
        # using freeze_time() to stop the time on 2016-01-01 and comparing the follow-up
        # report values with the expected values #T7127
        with freeze_time("2016-01-01"):
            account_move = self.env["account.move"].search(
                [("name", "=", "INV/2016/00001")]
            )
            for line in account_move.invoice_line_ids:
                # assertLinesValues() from TestAccountReportsCommon to
                # verify report values #T7127
                self.assertLinesValues(
                    report._get_followup_report_lines(options),
                    [0, 1, 2, 3, 4, 5, 6, 8],
                    [
                        (
                            "INV/2016/00001",
                            "01/01/2016",
                            "01/01/2016",
                            "",
                            "Brand_a",
                            "INV/2016/00001",
                        ),
                        ("", "", "", "", "", "Total Due", 500.00),
                    ],
                )
