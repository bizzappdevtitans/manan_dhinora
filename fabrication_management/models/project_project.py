from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    sale_order_ref = fields.Many2one(comodel_name="sale.order", string="Sales")
