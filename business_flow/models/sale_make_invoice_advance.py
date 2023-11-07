from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = ["sale.advance.payment.inv"]

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """inheriting this method to update the dict which creates incoice #T00379"""
        invoice_vals_wiz = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals_wiz.update({"customer_desc_invoice": order.customer_desc_invoice})
        return invoice_vals_wiz
