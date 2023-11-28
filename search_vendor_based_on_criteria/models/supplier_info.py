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
    def _get_sequence(self):
        """this method will assign a sequence value to all the product.supplierinfo
        records that dont already have one based on their id #T6979"""
        supplier_sequence = self.search([("supplier_sequence", "=", False)])
        for supplier in supplier_sequence:
            supplier.supplier_sequence = supplier.id

    @api.model
    def name_get(self):
        """using name_get to get the required name - price in the
        m2o in order_line #T00479"""
        final_name = [
            (
                supplier.id,
                "%s - %s %s"
                % (supplier.name.name, supplier.currency_id.symbol, supplier.price),
            )
            for supplier in self
        ]
        return final_name
