from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    welding_type = fields.Many2one(
        comodel_name="product.product",
        string="Preferd Welding",
        domain='[("welding", "=", True)]',
    )

    @api.onchange("welding_type")
    def welding_requirement(self):
        pass
