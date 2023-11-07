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
        supplierinfo = self.env["product.supplierinfo"]
        supplier_ids = supplierinfo.search([])
        for supplier in supplier_ids:
            if not supplier.supplier_sequence:
                supplier.write({"supplier_sequence": supplier.id})
            continue

    @api.depends("product_id")
    def _compute_supplier_id(self):
        """this compute method will give us the required product.supplierinfo id
        according to our criteria #T00479"""
        self.update_supplier_sequence()
        if self.product_id:
            sellers = self.product_id.mapped("seller_ids")
            # creating a dict of all the sellers of the selected product_id
            supplier_criteria_info = {}
            for supplier in self.env["product.supplierinfo"].browse(sellers.ids):
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
            criteria_ls = ["price", "delay", "supplier_sequence"]
            for criteria in criteria_ls:
                citeria_values = []
                for vendor in supplier_criteria_info:
                    citeria_values.append(
                        supplier_criteria_info.get(vendor).get(criteria)
                    )
                citeria_values.sort()
                required_vendor = list()
                for supplier_info in supplier_criteria_info:
                    if (
                        supplier_criteria_info.get(supplier_info).get(criteria)
                        == citeria_values[0]
                    ):
                        required_vendor.append(supplier_info)
                if not len(required_vendor) > 1:
                    self.supplier = supplier_criteria_info.get(required_vendor[0]).get(
                        "id"
                    )
                    return self.supplier
                # if there are more than one values the we continue to check for the
                # next field in criteria list
                continue
        return self.supplier
