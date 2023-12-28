from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Added new field #T7003
    seller_id = fields.Many2one(
        "res.partner",
        string="Product Seller",
    )
