from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    # adding field to account.move #T00379
    customer_desc_invoice = fields.Text(string="Customer Sale Description")
