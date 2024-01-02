from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def wiz_replenish_product(self):
        """New method to call the 'replenish_products' wizard from server
        action replenish_wizard_product_template #T7127"""
        return {
            "type": "ir.actions.act_window",
            "res_model": "replenish.products",
            "view_mode": "form",
            "views": [(False, "form")],
            "res_id": False,
            "target": "new",
        }
