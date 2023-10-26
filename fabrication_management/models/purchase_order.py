from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    description = fields.Text(string="Internal Description")
    sale_refrence = fields.Many2one(comodel_name="sale.order", string="Sales refrence")

    def action_sale_mrp_reference(self):
        return {
            "res_model": "sale.order",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.sale_refrence.id,
        }
