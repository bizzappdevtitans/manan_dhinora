from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    import_id = fields.Many2one(
        "import.customer",
        string="Imported from",
        ondelete="cascade",
    )
