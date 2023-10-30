from odoo import models


class StockMove(models.Model):
    _inherit = ["stock.move"]

    def _prepare_procurement_values(self):
        """inheriting this method to get values from stock.move to stock.rule #T00392"""
        return_vals = super(StockMove, self)._prepare_procurement_values()
        # using group_id.sale_id to get sale.order() in the dict
        return_vals.update(
            {
                "sale_order_purchase": self.group_id.sale_id,
                "sale_order_mrp": self.group_id.sale_id,
            }
        )
        return return_vals

    def _get_new_picking_values(self):
        """inheriting this method to pass the value to
        delivery order(stock.picking) #T00437"""
        rtn_vals = super(StockMove, self)._get_new_picking_values()
        # using self.group_id.sale_id.id to get the id of the sale order and
        # then browsing it for the required value
        rtn_vals["delivery_description"] = (
            self.env["sale.order"]
            .browse([self.group_id.sale_id.id])
            .delivery_description
        )
        return rtn_vals
