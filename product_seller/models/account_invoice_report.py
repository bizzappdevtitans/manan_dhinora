from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    # Added new field #T7003
    seller_id = fields.Many2one(
        comodel_name="res.partner",
        string="Product Seller",
    )

    @api.model
    def _select(self):
        """inheriting this method to modify the sql query which will set the value for
        seller_id according to the seller_id in product.product #T7003"""
        return (
            super(AccountInvoiceReport, self)._select()
            + ", product.seller_id AS seller_id"
        )
