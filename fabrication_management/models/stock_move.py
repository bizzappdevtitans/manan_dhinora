from odoo import models


class StockMove(models.Model):
    _inherit = ["stock.move"]

    def _prepare_procurement_values(self):
        return_vals = super(StockMove, self)._prepare_procurement_values()
        # using group_id.sale_id to get sale.order() in the dict
        return_vals.update({"sale_order": self.group_id.sale_id})
        return return_vals
