from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    # TODO write comments
    metal = fields.Boolean(string="is Metal")
    welding = fields.Boolean(string="Welding Technique")
