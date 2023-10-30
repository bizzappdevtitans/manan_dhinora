from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # declering a custom field to recive the value from sale.order #T00437
    delivery_description = fields.Text(string="Delivery description")
