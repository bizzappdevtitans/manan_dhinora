from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fab_job = fields.Boolean(string="fabrication")
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(
            {"maintenance_cycle": self.maintenance_cycle, "fab_job": self.fab_job}
        )
        return invoice_vals
