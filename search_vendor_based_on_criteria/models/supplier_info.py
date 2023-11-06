from odoo import fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    vendor_sequence = fields.Integer(string="Sequence")
