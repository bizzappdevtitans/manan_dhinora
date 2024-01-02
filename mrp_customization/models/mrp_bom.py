from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Added new field #T7141
    max_qty = fields.Float(
        string="Max Quantity",
    )
