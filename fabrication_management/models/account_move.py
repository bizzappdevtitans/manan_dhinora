from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    # TODO write comments
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")
    fab_job = fields.Boolean(string="Fabrication Job")

    def _maintenance_cycle_email_cron(self):
        invoice_ids = self.search([]).ids
        if invoice_ids:
            for invoice in invoice_ids:
                invoice_record = self.browse([invoice])
                if (
                    invoice_record.maintenance_cycle
                    and invoice_record.state == "posted"
                    and invoice_record.fab_job
                ):
                    template_id = self.env.ref(
                        "fabrication_managemant.maintenance_cycle_mail_template"
                    )
                    template_id.send_mail(invoice, force_send=True)
