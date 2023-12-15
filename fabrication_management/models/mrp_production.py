from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # to get the reference of partner_id from sale
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
