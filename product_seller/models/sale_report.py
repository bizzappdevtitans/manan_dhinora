from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    # Add new field #T7003
    seller_id = fields.Many2one(
        comodel_name="res.partner",
        string="Product seller",
    )

    def _select_sale(self, fields=None):
        """Inherited method used to modify the sql query which will set the value for
        seller_id according to the seller_id in product.product #T7003"""
        return (
            super(SaleReport, self)._select_sale(fields) + ",p.seller_id as seller_id"
        )

    def _group_by_sale(self, groupby):
        """Inherited method to add the seller_id to group_by #T7003"""
        return super(SaleReport, self)._group_by_sale(groupby) + ",p.seller_id"
