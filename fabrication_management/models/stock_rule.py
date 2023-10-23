from odoo import models


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    def _prepare_order_line(self, values):
        """creating a list of the ids that are to be created in purchase.order.line
        using the _prepare_purchase_order method #T00469"""
        sale_order_line = values[0].get("sale_order").order_line
        welding_id = sale_order_line.mapped("welding_type").mapped("product_tmpl_id")
        purchase_line = []
        if welding_id.ids:
            for required_items in welding_id.ids:
                bom_items = (
                    self.env["mrp.bom"]
                    .search([("product_tmpl_id", "=", required_items)])
                    .mapped("bom_line_ids")
                    .mapped("product_id")
                ).ids
                purchase_line = purchase_line + bom_items
            values = []
            for product in purchase_line:
                values.append(
                    (
                        0,
                        0,
                        {
                            "product_id": product,
                        },
                    )
                )
            return values

    def _prepare_purchase_order(self, company_id, origins, values):
        """inheriting this method to update the dict that is beeing passed to create
        purchase order, then updating it to create the required order_line #T00469"""
        passed_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        if self._prepare_order_line(values):
            passed_vals.update({"order_line": self._prepare_order_line(values)})
        return passed_vals
