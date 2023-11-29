from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    seller_id = fields.Many2one(
        "res.partner",
        string="Product Seller",
    )
