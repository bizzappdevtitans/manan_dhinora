from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    # refrence to Sale used for smart button
    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale Reference")

    def action_sale_view(self):
        return {
            "res_model": "sale.order",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.sale_id.id,
        }
