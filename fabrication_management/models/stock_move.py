from odoo import models


class StockMove(models.Model):
    _inherit = ["stock.move"]

    def _prepare_procurement_values(self):
        """inheriting this method to send the refrence of the required sale
        order to stock.rule #T00469"""
        return_vals = super(StockMove, self)._prepare_procurement_values()
        # return_vals.update({"mrp_purchase": self.group_id.stock_move_ids
        # .created_purchase_line_id.order_id})
        return return_vals
        # TODO pass smartbutton values
