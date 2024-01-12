from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # Added new fields #T7141
    child_order_qty = fields.Integer(compute="_compute_child_qty")
    parent_id = fields.Many2one(comodel_name="mrp.production")

    def split_mo_based_on_qty(self):
        """New method to split MO based on max_qty at mrp_bom and
        product_qty #T7141"""
        if self.parent_id:
            raise ValidationError(
                _(
                    "This order is already split from another order "
                    "can't split a splitted order."
                )
            )
        if (self.product_qty) % (self.bom_id.max_qty) != 0:
            raise ValidationError(
                _(
                    """The total child production orders is a fraction,
                    Try to adjust maximum quantity of the BoM or production quantity."""
                )
            )
        # canceling the current MO #T7141
        self.action_cancel()
        child_order_qty = int(self.product_qty / self.bom_id.max_qty)
        # creating child MO based on child_order_qty #T7141
        for child_order in range(child_order_qty):
            self.create(
                {
                    "product_id": self.product_id.id,
                    "bom_id": self.bom_id.id,
                    "product_qty": 1,
                    "origin": self.origin,
                    "parent_id": self.id,
                }
            )

    @api.depends("state")
    def _compute_child_qty(self):
        """New compute the number of child MO created #T7141"""
        for mrp in self:
            mrp.child_order_qty = mrp.search_count([("parent_id", "=", mrp.id)])

    def action_open_child_orders(self):
        """New Method called for smart button child orders #T7141"""
        self.ensure_one()
        return {
            "name": "Child Orders",
            "res_model": "mrp.production",
            "domain": [("parent_id", "=", self.id)],
            "view_mode": "tree,form",
            "target": "current",
            "type": "ir.actions.act_window",
        }
