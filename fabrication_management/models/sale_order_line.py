from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    welding_type = fields.Many2one(
        comodel_name="product.product",
        string="Preferd Welding",
        domain='[("welding", "=", True)]',
    )

    @api.onchange("welding_type")
    def validate_welding_type(self):
        prod = self.env["product.product"]
        if self.welding_type:
            if not prod.browse([self.welding_type]).welding:
                raise ValidationError(_("the selected welding type is not valid."))
