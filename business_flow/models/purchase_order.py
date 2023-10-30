from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    # Declaring a new field to recive the value passed from sale.order #T00392
    sale_purchase_description = fields.Text(string="Purchase Description")
