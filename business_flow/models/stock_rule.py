from odoo import models


class StockRule(models.Model):
    _inherit = ["stock.rule"]

    def _prepare_purchase_order(self, company_id, origins, values):
        """using the above value to pass the value from stock.rule
        to purchase.order #T00392"""
        passed_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        # updating the dict with the value from sale.order().sale_description
        # from the prepare_procurment_values dict
        passed_vals.update(
            {
                "sale_purchase_description": values[0]
                .get("sale_order_purchase")
                .sale_purchase_description
            }
        )
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
        """inheriting this method to then update its return dict anc add the custom
        value from sale_order #T00425"""
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
        # using the values dict to get the value of manufacturing_spec from sale.order
        return_dict_vals.update(
            {"manufacturing_spec": values.get("sale_order_mrp").manufacturing_spec}
        )
        return return_dict_vals
