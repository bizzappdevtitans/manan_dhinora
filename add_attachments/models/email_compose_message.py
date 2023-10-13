from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def attachments(self):
        """using a button to fetch all the required attachments to then add then
        to attachment_ids #T00464"""
        sale_order = self.env.context.get("active_id")
        attachment = self.env["ir.attachment"]
        products = self.env["sale.order"].browse([sale_order]).order_line.product_id
        template_products = []
        for product_temp in products.ids:
            template_ids = (
                self.env["product.product"].browse([product_temp]).product_tmpl_id
            )
            template_products.append(template_ids.id)
        # finding product attachments in product.product
        if len(products.ids) > 0:
            product_attachment = []
            for prod_product in products.ids:
                product_product_attachment = attachment.search(
                    [
                        ("res_model", "=", "product.product"),
                        ("res_id", "=", prod_product),
                    ]
                )
                for prod_product_attachment in product_product_attachment.ids:
                    product_attachment.append(prod_product_attachment)
        # finding product attachments in product.template
        if len(template_products) > 0:
            template_attachment = []
            for tmp_product in template_products:
                product_template_attachments = attachment.search(
                    [
                        ("res_model", "=", "product.template"),
                        ("res_id", "=", tmp_product),
                    ]
                )
                for tmp_product_attachment in product_template_attachments.ids:
                    template_attachment.append(tmp_product_attachment)
        # finding attachments in sale.order
        sale_attachment = attachment.search(
            [
                ("res_model", "=", "sale.order"),
                ("res_id", "=", sale_order),
            ]
        )
        # making a final list of all the product that are to be attached in the email
        net_attachment = sale_attachment.ids + product_attachment + template_attachment

        for i in net_attachment:
            self.write({"attachment_ids": [(4, i)]})
