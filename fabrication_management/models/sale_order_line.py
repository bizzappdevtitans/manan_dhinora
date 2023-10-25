from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    # TODO write comments
    welding_type = fields.Many2one(
        comodel_name="product.product",
        string="Preferd Welding",
        domain='[("welding", "=", True)]',
    )
