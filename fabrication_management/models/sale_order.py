from datetime import datetime, timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # TODO write comments
    fab_job = fields.Boolean(string="fabrication")
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")
    purchase_refrence = fields.Many2one(
        comodel_name="purchase.order", string="Purchase refrence"
    )

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(
            {"maintenance_cycle": self.maintenance_cycle, "fab_job": self.fab_job}
        )
        return invoice_vals

    def _prepare_po_vals(self, variant_ids, varaint_qty):
        """this method wil be called when we are needed to create a purchase order
        for a product.template record with multiple variants #T00469"""
        values = []
        for variant in range(len(variant_ids)):
            if varaint_qty[variant] > 0:
                values.append(
                    (
                        0,
                        0,
                        {
                            "product_id": variant_ids[variant],
                            "product_qty": varaint_qty[variant],
                        },
                    )
                )
        return values

    def _replenish_welding_materials_cron(self):
        welding_types = self.env["product.product"].search([("welding", "=", True)])
        vals = []
        po_vendor = []
        for welding in welding_types:
            sale_line = (
                self.search([])
                .filtered(
                    lambda record: record.date_order
                    > (datetime.now() - timedelta(days=7))
                )
                .mapped("order_line")
                .filtered(lambda rec: rec.welding_type.id == welding.id)
            )
            sale_line_qty = sum(sale_line.mapped("product_uom_qty"))
            sale_line_welding_type = sale_line.mapped("welding_type").mapped(
                "product_tmpl_id"
            )
            bom_line = (
                self.env["mrp.bom"]
                .search([("product_tmpl_id", "=", sale_line_welding_type.id)])
                .mapped("bom_line_ids")
            )
            po_product = bom_line.mapped("product_id")
            weld_req_qty = bom_line.mapped("product_qty")
            so_product_qty = []
            for item in weld_req_qty:
                so_product_qty.append(item * sale_line_qty)
            po_product_qty = []
            for product in po_product.ids:
                purchase_line_product = (
                    self.env["purchase.order.line"]
                    .search([("product_id", "=", product)])
                    .mapped("product_qty")
                )
                po_product_qty.append(sum(purchase_line_product))
            net_procurement_qty = []
            for index in range(len(so_product_qty)):
                final_qty = so_product_qty[index] - po_product_qty[index]
                net_procurement_qty.append(final_qty)

            vals = vals + self._prepare_po_vals(po_product.ids, net_procurement_qty)
            po_vendor = po_vendor + (po_product.mapped("seller_ids").mapped("name")).ids
        if vals:
            self.env["purchase.order"].create(
                {
                    "partner_id": po_vendor[0],
                    "order_line": vals,
                    "description": "created due to replenishment",
                }
            )

    def action_mrp_po_refrence(self):
        return {
            "res_model": "purchase.order",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.purchase_refrence.id,
        }

    def prepare_project_vals(self):
        vals = {}
        partner = self.partner_id
        end_date = self.date_order + timedelta(
            days=int(self.env["ir.config_parameter"].get_param("project_deadline"))
        )
        vals["name"] = str(partner.mapped("name")[0]) + " - " + str(self.date_order)
        vals["partner_id"] = partner.id
        vals["date_start"] = self.date_order
        vals["date"] = end_date
        vals["sale_order_ref"] = self.id
        return vals

    def prepare_task_vals(self):
        order_line = self.order_line.ids
        project_id = self.env["project.project"].search(
            [("sale_order_ref", "=", self.id)]
        )
        vals = []
        for job in order_line:
            values = {}
            product_id = self.order_line.browse([job]).mapped("product_id")
            values["project_id"] = project_id.id
            values["name"] = product_id.name + " - " + self.partner_id.mapped("name")[0]
            values["partner_id"] = self.partner_id.id
            values["kanban_state"] = "normal"
            values["sale_ref"] = self.id
            values["date_deadline"] = self.date_order + timedelta(
                days=int(self.env["ir.config_parameter"].get_param("project_deadline"))
            )
            vals.append(values)
        return vals

    def _action_confirm(self):
        return_vals = super(SaleOrder, self)._action_confirm()
        self.env["project.project"].create(self.prepare_project_vals())
        vals = self.prepare_task_vals()
        for task in vals:
            self.env["project.task"].create(task)
        return return_vals

    def action_project_view(self):
        project_id = self.env["project.project"].search(
            [("sale_order_ref", "=", self.id)]
        )
        return {
            "res_model": "project.project",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": project_id,
        }

    def action_task_view(self):
        return {
            "res_model": "project.task",
            "view_mode": "tree,form",
            "type": "ir.actions.act_window",
            "domain": [("sale_ref.id", "=", self.id)],
        }
