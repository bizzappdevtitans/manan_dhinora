from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    metal = fields.Boolean(string="is Metal")
    welding = fields.Boolean(string="Welding Technique")
