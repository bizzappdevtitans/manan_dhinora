from odoo import models


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    def _prepare_purchase_order(self, company_id, origins, values):
        """inheriting this method to update the dict that is beeing passed to create
        purchase order, then updating it to create the required order_line #T00469"""
        passed_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        passed_vals.update({"sale_refrence": values[0].get("sale_order")})
        return passed_vals

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        """using this method to pass value to mrp.production #T00469"""
        return_dict_vals = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        # using the values dict to get the value of partner from sale.order
        return_dict_vals.update({"partner_id": values.get("mrp_partner").partner_id.id})
        return return_dict_vals
