from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
