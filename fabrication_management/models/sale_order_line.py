from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # this field wil let us choose prefered welding type at order_line level
    welding_type = fields.Many2one(
        comodel_name="product.product",
        string="Preferd Welding",
        domain='[("welding", "=", True)]',
    )
