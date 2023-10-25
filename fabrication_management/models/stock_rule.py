from odoo import models


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    def _prepare_purchase_order(self, company_id, origins, values):
        """inheriting this method to update the dict that is beeing passed to create
        purchase order, then updating it to create the required order_line #T00469"""
        passed_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        passed_vals.update({"description": values[0].get("mrp_purchase").description})
        return passed_vals
        # TODO pass smartbutton values
