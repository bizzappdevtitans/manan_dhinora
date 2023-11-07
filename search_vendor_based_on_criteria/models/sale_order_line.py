from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    supplier = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Vendor",
        compute="_compute_supplier_id",
    )

    def update_supplier_sequence(self):
        """this method will be called every time we change the product_id and write
        sequence value based on product.supplierinfo.id,
         if the sequence field is empty #T00479"""
        for supplier in self.env["product.supplierinfo"].search(
            [("supplier_sequence", "=", False)]
        ):
            if not supplier.supplier_sequence:
                supplier.write({"supplier_sequence": supplier.id})

    @api.depends("product_id")
    def _compute_supplier_id(self):
        """this compute method will give us the required product.supplierinfo id
        according to our criteria #T00479"""
        if not self.product_id:
            return self.supplier
        # updating all the partner.supplierinfo who doesn't have a sequence
        self.update_supplier_sequence()
        # creating a dict of all the sellers of the selected product_id
        supplier_criteria_info = {}
        for supplier in self.env["product.supplierinfo"].browse(
            self.product_id.mapped("seller_ids").ids
        ):
            supplier_criteria_info[supplier.name.name] = {
                "price": supplier.price,
                "delay": supplier.delay,
                "supplier_sequence": supplier.supplier_sequence,
                "id": supplier.id,
            }
        # if number of sellers is 1 or less, we just assign them directly
        if not len(supplier_criteria_info) > 1:
            return self.supplier
        # fields to be checked in their priority order
        for criteria in ["price", "delay", "supplier_sequence"]:
            citeria_values = []
            for vendor in supplier_criteria_info:
                citeria_values.append(supplier_criteria_info.get(vendor).get(criteria))
            citeria_values.sort()
            required_vendor = [
                supplier_info
                for supplier_info in supplier_criteria_info
                if (
                    supplier_criteria_info.get(supplier_info).get(criteria)
                    == citeria_values[0]
                )
            ]
            if not len(required_vendor) > 1:
                self.supplier = supplier_criteria_info.get(required_vendor[0]).get("id")
                return self.supplier
