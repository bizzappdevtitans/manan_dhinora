# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    seller_id = fields.Many2one(
        "res.partner",
        string="Product Saller",
    )

    @api.model
    def _select(self):
        """inheriting this method to modify the sql query which will set the value for
        seller_id according to the seller_id in product.product #T7003"""
        # TODO add the sql query to return string
        # for fetching the seller_id from product.product
        return super(AccountInvoiceReport, self)._select()
