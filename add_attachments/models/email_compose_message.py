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
        for product_temp in products:
            template_ids = (
                self.env["product.product"].browse([product_temp]).product_tmpl_id
            )
            template_products.append(template_ids.id)
        # finding product attachments in the product.product object
        if len(products.ids) > 0:
            product_attachment = []
            for prod_product in products.ids:
                product_product_attachment = attachment.search(
                    [
                        ("res_model", "=", "product.product"),
                        ("res_id", "=", prod_product),
                    ]
                )
                product_attachment.append(product_product_attachment)
        # finding product attachments in product.template object
        if len(template_products) > 0:
            template_attachment = []
            for tmp_product in template_products:
                product_template_attachment = attachment.search(
                    [
                        ("res_model", "=", "product.template"),
                        ("res_id", "=", tmp_product),
                    ]
                )
                template_attachment.append(product_template_attachment.id)
        # finding attachments in sale.order object
        sale_attachment = attachment.search(
            [
                ("res_model", "=", "sale.order"),
                ("res_id", "=", sale_order),
            ]
        )
        # making a list of all the product that are to be attached in the
        # action_quotation_send method
        net_attachment = (
            sale_attachment + product_product_attachment + product_template_attachment
        )
        self.write({"attachment_ids": net_attachment})
