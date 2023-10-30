from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project_prepare_values(self):
        """inheriting this method to get the value from sale.order.line to
        project.project T00422"""
        return_vals = super(
            SaleOrderLine, self
        )._timesheet_create_project_prepare_values()
        # using order_id to get the value from sale.order to sale.order.line
        return_vals.update({"project_description": self.order_id.project_description})
        return return_vals

    def _timesheet_create_task_prepare_values(self, project):
        """inheriting this method to get the value from sale.order.line to
        project.task T00422"""
        return_vals = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        # using order_id to get the value from sale.order to sale.order.line
        return_vals.update(
            {"project_task_description": self.order_id.project_task_description}
        )
        return return_vals
