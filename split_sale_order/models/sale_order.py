from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # required field for refrence to parent sale order
    source_sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Split Refrence"
    )

    def action_split_quotation_wiz(self):
        """this method will return a wizard thich can be used to split the sale
        order #T00480"""
        # validating if the record is splitable or not
        if not self.state == "draft":
            raise ValidationError(_("The order is not in draft state"))
        elif self.source_sale_order_id:
            raise ValidationError(
                _(
                    "Cannot split a sale order, which was splitted from another sale order"
                )
            )
        return {
            "type": "ir.actions.act_window",
            "res_model": "split.quotation",
            "view_mode": "form",
            "target": "new",
        }
