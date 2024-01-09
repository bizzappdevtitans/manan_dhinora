from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Added new field #T7127
    product_brand_id = fields.Many2one(
        "product.brand",
        related="product_id.product_brand_id",
        string="Brand",
    )
