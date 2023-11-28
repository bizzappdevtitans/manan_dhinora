from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # declaring required field
    supplier_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Vendor",
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """this onchange method will fetch the required supplier_ids and get the
        required id based on the 'order' and 'limit' parameters T6979"""
        for order_line in self:
            if order_line.product_id.seller_ids:
                order_line.supplier_id = (
                    self.env["product.supplierinfo"].search(
                        [("id", "in", self.product_id.seller_ids.ids)],
                        order="price asc, delay asc, supplier_sequence asc",
                        limit=1,
                    )
                ).id
