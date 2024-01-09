from odoo import fields, models


class product_brand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"
    _rec_name = "name"

    # Added new field #T7127
    name = fields.Char()
    product_ids = fields.One2many(
        comodel_name="product.product",
        inverse_name="product_brand_id",
    )
