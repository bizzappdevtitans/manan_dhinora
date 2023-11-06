from odoo import api, fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    # decalring field
    all_attachments = fields.Boolean(string="Add all attachment")

    @api.onchange("all_attachments")
    def add_extra_attachments(self):
        """this method will check for all the attached files in the currnet sale order,
        and then based or if the all_attachment field is true it, will write or unlink
        the m2m field(attachment_ids) #T00464"""
        sale_attachment = (
            self.env["ir.attachment"]
            .search(
                [
                    ("res_model", "=", "sale.order"),
                    ("res_id", "=", self.env.context.get("active_id")),
                ]
            )
            .ids
        )
        if self.all_attachments:
            for attachment_id in sale_attachment:
                self.write({"attachment_ids": [(4, attachment_id)]})

        elif not self.all_attachments:
            # if the user manually stes the field to false the extra attachments
            # that were added will be unlinked
            for attachment_id in sale_attachment:
                if attachment_id in self.attachment_ids.ids:
                    self.write({"attachment_ids": [(3, attachment_id, 0)]})
