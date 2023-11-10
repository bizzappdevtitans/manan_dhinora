from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SplitQuotation(models.TransientModel):
    _name = "split.quotation"
    _description = "Split Quotation"

    split_order = fields.Boolean(string="Split Based on Category")

    def action_split_quotation(self):
        """we split the order_line according to category #T00480"""
        for record in self:
            sale_id = record.env["sale.order"].browse(
                [record.env.context.get("active_id")]
            )
            if not record.split_order:
                raise ValidationError(_("The split option is not selected"))
            order_lines = sale_id.mapped("order_line")
            # preparing a dict of order_line according to their product category
            line_ids_category = {}
            for line_category in order_lines.mapped("product_id").mapped("categ_id"):
                order_line_ls = []
                for line in order_lines:
                    if line.mapped("product_id").mapped("categ_id") == line_category:
                        order_line_ls.append(line.id)
                line_ids_category[line_category.name] = order_line_ls
            # creating new sale order according to the dict
            for category in line_ids_category:
                self.env["sale.order"].create(
                    {
                        "partner_id": sale_id.partner_id.id,
                        "source_sale_order_id": sale_id.id,
                        "order_line": [(6, 0, line_ids_category.get(category))],
                    }
                )
                # as using [(6, [IDs])] will unlink ids from original(parent) sale order
                # we are creating a copy of these ids and writing them in the parent SO
                for line_value in self.env["sale.order.line"].browse(
                    line_ids_category.get(category)
                ):
                    sale_id.write(
                        {
                            "order_line": [
                                (
                                    0,
                                    0,
                                    {
                                        "product_id": line_value.product_id.id,
                                        "product_uom_qty": line_value.product_uom_qty,
                                        "price_unit": line_value.price_unit,
                                        "order_id": sale_id.id,
                                    },
                                ),
                            ]
                        }
                    )
