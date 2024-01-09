from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # Added new field #T7127
    product_brand_id = fields.Many2one(
        "product.brand",
        string="Brand",
        ondelete="cascade",
        related="product_id.product_brand_id",
    )
