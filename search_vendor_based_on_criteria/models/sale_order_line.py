from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # declaring required field
    supplier_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Vendor",
        compute="_compute_supplier_id",
    )

    def _update_supplier_sequence(self):
        """this method will be called every time we change the product_id and write
        sequence value based on product.supplierinfo.id,
         if the sequence field is empty #T00479"""
        for supplier in self.env["product.supplierinfo"].search(
            [("supplier_sequence", "=", False)]
        ):
            if not supplier.supplier_sequence:
                supplier.write({"supplier_sequence": supplier.id})

    def _fetch_supplier_id(self, product_id, self_id):
        """this method will be called every time we need to find the supplier_id based
        on the required criteria, to assign to the compute field #T00479"""
        self_record = self.search([("id", "=", self_id)])
        product_id = self.env["product.product"].search([("id", "=", product_id)])
        supplier_ids = (
            self.env["product.supplierinfo"].browse(product_id.mapped("seller_ids")).ids
        )
        # preparing a dict of all the availabe seller_ids for this product_id
        supplier_criteria_info = {
            supplier.name.name: {
                "price": supplier.price,
                "delay": supplier.delay,
                "supplier_sequence": supplier.supplier_sequence,
                "id": supplier.id,
            }
            for supplier in supplier_ids
        }
        # if number of sellers is 1 or less, we just assign them directly
        if len(supplier_criteria_info) == 1:
            if self_id:
                return self_record.write(
                    {"supplier_id": product_id.mapped("seller_ids").id}
                )
            self.supplier_id = supplier_ids[0]
            return self.supplier_id
        # fields to be checked based on following criteria, in this priority order
        for criteria in ["price", "delay", "supplier_sequence"]:
            citeria_values = [
                supplier_criteria_info.get(vendor).get(criteria)
                for vendor in supplier_criteria_info
            ]
            required_vendor = [
                supplier_info
                for supplier_info in supplier_criteria_info
                if (
                    supplier_criteria_info.get(supplier_info).get(criteria)
                    == citeria_values[0]
                )
            ]
            if len(required_vendor) == 1:
                if self_id:
                    return self_record.write(
                        {
                            "supplier_id": supplier_criteria_info.get(
                                required_vendor[0]
                            ).get("id")
                        }
                    )
                self.supplier_id = supplier_criteria_info.get(required_vendor[0]).get(
                    "id"
                )
                return self.supplier_id

    @api.depends("product_id")
    def _compute_supplier_id(self):
        """this compute method will give us the required product.supplierinfo id
        according to our criteria #T00479"""
        if not self.product_id or self.supplier_id:
            return self.supplier_id
        self._update_supplier_sequence()
        if len(self.product_id) == 1:
            # as when there is only one order line we will not get a case with ,
            # multiple product_id, so we dont need self_id
            return self._fetch_supplier_id(self.product_id.id, False)
        for record in zip(self.product_id.ids, self.ids):
            (product_id, self_id) = record
            self._fetch_supplier_id(product_id, self_id)
