from odoo import api, fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    # declaring required field
    supplier_sequence = fields.Integer(string="Supplier ID")

    _sql_constraints = [
        (
            "unique_supplier_sequence",
            "UNIQUE(supplier_sequence)",
            "This sequence value is already used",
        )
    ]

    @api.model
    def name_get(self):
        """using name_get to get the required name - price in the
        m2o in order_line #T00479"""
        final_name = []
        for supplier in self:
            final_name.append(
                (
                    supplier.id,
                    "%s - %s %s"
                    % (supplier.name.name, supplier.currency_id.symbol, supplier.price),
                )
            )
        return final_name
