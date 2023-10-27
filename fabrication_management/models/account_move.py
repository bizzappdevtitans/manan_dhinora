from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    # this field if set to true will run the ir_cron_maintenance_cycle_mail cron job
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")
    # as company_id and email required in sending email
    company_id = fields.Many2one(
        "res.company",
        "Company",
        default=lambda self: self.env.company,
        index=True,
        required=True,
    )

    def _maintenance_cycle_email_cron(self):
        """this method is called when to cron ir_cron_maintenance_cycle_mail is running,
        it gives record ids to send email to as well as the email template #T00469"""
        invoice_ids = self.search([]).ids
        if invoice_ids:
            for invoice in invoice_ids:
                invoice_record = self.browse([invoice])
                if (
                    invoice_record.maintenance_cycle
                    and invoice_record.state == "posted"
                ):
                    self.env.ref(
                        "fabrication_management.maintenance_cycle_mail_template"
                    ).send_mail(invoice, force_send=True)
