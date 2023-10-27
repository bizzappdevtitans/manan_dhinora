from datetime import datetime, timedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # TODO write comments
    maintenance_cycle = fields.Boolean(string="Opt for maintenance")

    metal_used = fields.Many2one(
        comodel_name="product.product", string="Metals Used", compute="_compute_metals"
    )
    # these fields are used to count total number of tasks generated for smart button
    task_length = fields.Integer(compute="_compute_task_amount")
    task_ids = fields.One2many(comodel_name="project.task", inverse_name="sale_ref")

    @api.depends("order_line")
    def _compute_metals(self):
        """this compute method will find the metal used based on BOM #T00469"""
        if self.order_line:
            products = []
            # getting products_id for products in sale.order.line
            for order in self:
                line_product = order.order_line.mapped("product_id")
                products = products + line_product.ids
            # getting the product_id of metal used from bom
            for item in products:
                tmpl_id = self.env["product.product"].browse([item]).product_tmpl_id
                metal = (
                    self.env["mrp.bom"]
                    .search([("product_tmpl_id", "=", tmpl_id.id)])
                    .mapped("bom_line_ids")
                    .mapped("product_id")
                    .filtered(lambda item: item.metal is True)
                )
                order.metal_used = metal[0]
            return self.metal_used
        return self.metal_used

    def _prepare_invoice(self):
        """passing the value of the maintenance_cycle field to invoice #T00469"""
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(
            {
                "maintenance_cycle": self.maintenance_cycle,
            }
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
        """this code for cron job will check for number of welding products and type
        of welding, based on this will find the sale to purchase difference and make
        a PO accordingly #T00469"""
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
            # getting the types of welding used and number of their instances in SO
            sale_line_qty = sum(sale_line.mapped("product_uom_qty"))
            sale_line_welding_type = sale_line.mapped("welding_type").mapped(
                "product_tmpl_id"
            )
            bom_line = (
                self.env["mrp.bom"]
                .search([("product_tmpl_id", "=", sale_line_welding_type.id)])
                .mapped("bom_line_ids")
            )
            # getting the bom for welding to get the list of required products in PO
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
            # calculating the total required quantity to make a purchase order
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

    def prepare_project_vals(self):
        """this method is called to make a dict of values needed to
        create a project.project record #T00469"""
        partner = self.partner_id
        # getting the end date for project, this date can be changed in system parameter
        end_date = self.date_order + timedelta(
            days=int(self.env["ir.config_parameter"].get_param("project_deadline"))
        )
        return {
            "name": str(partner.mapped("name")[0]) + " - " + str(self.date_order),
            "partner_id": partner.id,
            "date_start": self.date_order,
            "date": end_date,
            "sale_order_ref": self.id,
        }

    def _prepare_task_vals(self):
        """this method is called to make a dict of values needed to
        create project.task records #T00469"""
        order_line = self.order_line.ids
        # finding the parent project id from the sale order refrence passed
        project_id = self.env["project.project"].search(
            [("sale_order_ref", "=", self.id)]
        )
        vals = []
        # as there can be multiple order_line so we create multiple tasks
        for job in order_line:
            product_id = self.order_line.browse([job]).mapped("product_id")
            # getting the enddate which is controlled by the same
            # system parameter as the project
            end_date = self.date_order + timedelta(
                days=int(self.env["ir.config_parameter"].get_param("project_deadline"))
            )
            values = {
                "project_id": project_id.id,
                "name": product_id.name + " - " + self.partner_id.mapped("name")[0],
                "partner_id": self.partner_id.id,
                "kanban_state": "normal",
                "sale_ref": self.id,
                "date_deadline": end_date,
            }
            vals.append(values)
        return vals

    def _action_confirm(self):
        """inheriting this method to add the project and task creation
        method calls #T00469"""
        return_vals = super(SaleOrder, self)._action_confirm()
        self.env["project.project"].create(self.prepare_project_vals())
        for task in self._prepare_task_vals():
            self.env["project.task"].create(task)
        return return_vals

    def action_project_view(self):
        """smart button to show the project created #T00469"""
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
        """smart button to show the tasks created by the current SO #T00469"""
        return {
            "res_model": "project.task",
            "view_mode": "tree,form",
            "type": "ir.actions.act_window",
            "domain": [("sale_ref.id", "=", self.id)],
        }

    @api.depends("task_ids")
    def _compute_task_amount(self):
        """this method is used to count the number of tasks created to show in
        the oe_stat widget #T00469"""
        self.task_length = len(self.task_ids)
