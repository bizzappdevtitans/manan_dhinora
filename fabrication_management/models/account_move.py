from odoo import fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    # adding field to account.move
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")
    fab_job = fields.Boolean(string="Fabrication Job")

    def _maintenance_cycle_email_cron(self):
        if self.maintenance_cycle and self.state == "posted" and self.fab_job:

            # logic to create an email
            pass
