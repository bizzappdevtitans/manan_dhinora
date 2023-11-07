from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    # adding field to sale.order to pass a value to invoice #T00379
    customer_desc_invoice = fields.Text(string="Invoice description")
    # declaring a new field to pass a custom value from sale to purchase #T00392
    sale_purchase_description = fields.Text(string="Purchase Description")
    # field to pass value from sale to project #T00422
    project_description = fields.Text(string="Project description")
    # field used to pass value from SO to project/task #T00422
    project_task_description = fields.Text(string="Task description")
    # field to pass value from sale to mrp #T00425
    manufacturing_spec = fields.Text(string="Manufacturing description")
    # field to pass value from sale to delivery  #T00437
    delivery_description = fields.Text(string="Delivery description")

    def _prepare_invoice(self):
        """inheriting this method update the dict that creats invoice #T00379"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({"customer_desc_invoice": self.customer_desc_invoice})
        return invoice_vals
