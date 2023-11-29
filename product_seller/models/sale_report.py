from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    seller = fields.Many2one(
        "res.partner",
        string="Product seller",
    )

    def _select_sale(self, fields=None):
        """inheriting this method to modify the sql query which will set the value for
        seller_id according to the seller_id in product.product #T7003"""
        return super(SaleReport, self)._select_sale(fields) + ",p.seller_id as seller"

    def _group_by_sale(self, groupby):
        """inheriting this method to add the seller_id to group_by #T7003"""
        return super(SaleReport, self)._group_by_sale(groupby) + ",p.seller_id"
