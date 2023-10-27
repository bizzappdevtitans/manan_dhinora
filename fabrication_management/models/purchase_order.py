from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # description field will be updated as the cron to replenish is finished running
    description = fields.Text(string="Internal Description")
    sale_refrence = fields.Many2one(comodel_name="sale.order", string="Sales refrence")

    def action_sale_mrp_reference(self):
        """this method is an action for a smart button to sale order which created the
        MO which created the current PO #T00469"""
        return {
            "res_model": "sale.order",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.sale_refrence.id,
        }
