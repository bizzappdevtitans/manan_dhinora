from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Added new field #T7127
    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Product Brand",
    )

    def wiz_replenish_product_variants(self):
        """New method call the wizard from the server action
        'replenish_wizard_product_variant' #T7127"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "replenish.products",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_id": False,
            "target": "new",
        }
