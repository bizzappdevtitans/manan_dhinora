from odoo import fields, models


class SplitQuotation(models.TransientModel):
    _name = "split.quotation"
    _description = "Split Quotation"

    split_order = fields.Selection(
        [
            ("category", "Category"),
            ("selected_line", "Selected Line"),
            ("per_order_line", "Per Line"),
        ],
        string="Split Based on",
    )
    # TODO create a proper m2m
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="active sale order",
        default=lambda sale_order: sale_order.env.context.get("active_id"),
        store=True,
    )
    sale_order_line_ids = fields.Many2many(
        comodel_name="sale.order.line",
        relation="order_line_ids_rel",
        default=lambda sale_order: sale_order.env["sale.order"]
        .browse([sale_order.env.context.get("active_id")])
        .order_line,
        string="Selected Lines",
    )

    def _category_split(self, sale_order_id):
        """we split the order_line according to category #T00480"""
        order_lines = sale_order_id.mapped("order_line")
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
                    "partner_id": sale_order_id.partner_id.id,
                    "source_sale_order_id": sale_order_id.id,
                    "order_line": [(6, 0, line_ids_category.get(category))],
                }
            )
            # as using [(6, [IDs])] will unlink ids from original(parent) sale order
            # we are creating a copy of these ids and writing them in the parent SO
            for line_value in self.env["sale.order.line"].browse(
                line_ids_category.get(category)
            ):
                sale_order_id.write(
                    {
                        "order_line": [
                            (
                                0,
                                0,
                                {
                                    "product_id": line_value.product_id.id,
                                    "product_uom_qty": line_value.product_uom_qty,
                                    "price_unit": line_value.price_unit,
                                    "order_id": sale_order_id.id,
                                },
                            ),
                        ]
                    }
                )

    def _selected_line_split(self, sale_order_id):
        """this method will be called when the selection field is set to selected
        order_lines #T00480"""
        line_ids = self.sale_order_line_ids
        vals = [
            (
                0,
                0,
                {
                    "product_id": line_id.product_id.id,
                    "product_uom_qty": line_id.product_uom_qty,
                    "price_unit": line_id.price_unit,
                    "order_id": sale_order_id.id,
                },
            )
            for line_id in line_ids
        ]
        self.env["sale.order"].create(
            {"partner_id": sale_order_id.partner_id.id, "order_line": vals}
        )

    def _per_line_split(self, sale_order_id):
        """this method will be called when the option per_line is selected
        i.e every order_line will make 1 sale order #T00480"""
        order_line_ids = sale_order_id.mapped("order_line")
        for line in order_line_ids:
            self.env["sale.order"].create(
                {
                    "partner_id": sale_order_id.partner_id.id,
                    "source_sale_order_id": sale_order_id.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "product_uom_qty": line.product_uom_qty,
                                "price_unit": line.price_unit,
                                "order_id": sale_order_id.id,
                            },
                        )
                    ],
                }
            )

    def action_split_quotation(self):
        """this action will be called when the split button is clicked and will split
        the sale_order based on the option selected in split_order field #T00480"""
        for record in self:
            sale_order_id = record.env["sale.order"].browse(
                [record.env.context.get("active_id")]
            )
            if record.split_order == "category":
                record._category_split(sale_order_id)
            elif record.split_order == "per_order_line":
                record._per_line_split(sale_order_id)
            else:
                record._selected_line_split(sale_order_id)
