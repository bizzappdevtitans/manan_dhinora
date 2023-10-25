from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = ["sale.advance.payment.inv"]

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """TODO write comments"""
        invoice_vals_wiz = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals_wiz.update(
            {"maintenance_cycle": order.maintenance_cycle, "fab_job": order.fab_job}
        )
        return invoice_vals_wiz
