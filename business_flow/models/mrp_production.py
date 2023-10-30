from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # declering a custom field in mrp.production to get the passed value #T00425
    manufacturing_spec = fields.Text(string="Sale Description")
