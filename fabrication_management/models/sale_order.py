from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fab_job = fields.Boolean(string="fabrication")
    welding_type = fields.Many2one(
        comodel_name="product.product",
        string="Preferd Welding",
        domain='[("welding", "=", True)]',
    )
