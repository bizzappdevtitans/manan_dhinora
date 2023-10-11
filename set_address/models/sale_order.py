from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """here we are checking how many partners are there whose bool field valid
        address is true base on that assigning the proper delivery address #T00455"""
        return_dict = super(SaleOrder, self).onchange_partner_id()
        partner = self.env["res.partner"]
        # checking if the input partner is a company
        if partner.browse([self.partner_id.id]).is_company is True:
            # fetching the child ids of the entered partner_id
            child_ids = partner.browse([self.partner_id.id]).child_ids
            partners_delivery = child_ids.filtered(
                lambda partner: partner.type == "delivery"
            )
            if len(partners_delivery.ids) > 0:
                partners_delivery_varified = partners_delivery.filtered(
                    lambda partner: partner.varified_address is True
                )
                if not len(partners_delivery_varified.ids) >= 1:
                    partners_dropship = child_ids.filtered(
                        lambda partner: partner.type == "drop_ship"
                    )
                    if len(partners_dropship.ids) > 0:
                        return_value = partners_dropship.ids[0]
                return_value = partners_delivery_varified.ids[0]
                self.with_company(self.company_id).update(
                    {"partner_shipping_id": return_value}
                )
        return return_dict
