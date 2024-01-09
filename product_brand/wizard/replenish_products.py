from odoo import fields, models


class ReplienishProducts(models.TransientModel):
    _name = "replenish.products"
    _description = "replenish products"

    # Added new field #T7127
    partner_id = fields.Many2one(
        "res.partner",
        string="Vendor",
    )
    product_qty = fields.Integer(
        string="Quantity",
    )

    def _create_po(self, records, brand):
        """New generic method to create purchse order based on selected records and
        the product_brand_id #T7127"""
        self.env["purchase.order"].create(
            {
                "partner_id": self.partner_id.id,
                "order_line": [
                    (
                        (
                            0,
                            0,
                            {
                                "product_id": record,
                                "product_qty": self.product_qty,
                            },
                        )
                    )
                    # using list comprihension to create all the PO lines based on the
                    # "brand" id #T7127
                    for record in (
                        records.filtered(
                            lambda prod: (prod.product_brand_id).id == brand
                        )
                    )
                ],
            }
        )

    def prepare_po_vals(self):
        """New method to create new purchase orders based on the brands of
        the selected products #T7127"""
        active_model = self.env.context.get("active_model")
        selected_records = self.env[active_model].browse(
            self.env.context.get("active_ids", [])
        )
        if active_model == "product.template":
            selected_records = selected_records.product_variant_id
        brad_ids = (selected_records.mapped("product_brand_id")).ids
        # if there is a product with no brand this condition will add 'False'
        # in the brand_ids list to create a PO for products without brand #T7127
        no_brand_records = selected_records.filtered(
            lambda prod: prod.product_brand_id is False
        )
        if no_brand_records:
            self._create_po(self, no_brand_records, False)
        for brand in brad_ids:
            self._create_po(self, selected_records, brand)
