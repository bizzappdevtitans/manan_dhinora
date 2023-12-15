from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    # refrence to sale_order used for smart buttons
    sale_order_ref = fields.Many2one(
        comodel_name="sale.order", string="Source Document"
    )
