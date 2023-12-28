from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    # Added new field #T7003
    seller_id = fields.Many2one(
        comodel_name="res.partner",
        string="Product Seller",
    )

    def _select(self):
        """Inherited method to modify the sql query which will set the value for
        seller_id according to the seller_id in product.product #T7003"""
        return super(PurchaseReport, self)._select() + ",p.seller_id as seller_id"

    def _group_by(self):
        """Inherited method to add the seller_id to group_by #T7003"""
        return super(PurchaseReport, self)._group_by() + ",p.seller_id"
