from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    # adding required fields
    type = fields.Selection(
        selection_add=[('drop_ship', 'Drop Shipping address'), ('other',)]
    )
    varified_address = fields.Boolean(string="Verified Address")
