from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_ref = fields.Many2one(comodel_name="sale.order", string="Sale Reference")

    def action_sale_view(self):
        return {
            "res_model": "sale.order",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.sale_ref.id,
        }
