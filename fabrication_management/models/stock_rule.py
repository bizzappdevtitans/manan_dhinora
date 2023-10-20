from odoo import models


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    def _prepare_purchase_order(self, company_id, origins, values):
        passed_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        passed_vals.update({"welding_type": values[0].get("sale_order").welding_type})
        return passed_vals
