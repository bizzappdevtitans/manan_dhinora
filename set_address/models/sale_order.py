from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def delivery_address(self):
        """here we are checking how many partners are there whose bool field valid
        address is true base on that assigning the proper delivery address #T00455"""
        partner = self.env["res.partner"]
        # searching for all the companies in res.partner
        companies = partner.search([["is_company", "=", True]])
        # checking if the input partner is a company or an individual
        if self.partner_id.id in companies.ids:
            # finding the employees in input company
            child_ids = partner.browse([self.partner_id.id]).child_ids
            varified_address_employee = []
            # searching for the employees whose boolean field is set to True
            for employee in child_ids.ids:
                if partner.browse([employee]).varified_address is True:
                    varified_address_employee.append(employee)
            # checking the number of records found if number> 0 procede
            # else let the original flow function
            if len(varified_address_employee) > 0:
                # checking if there is one or multiple records
                if len(varified_address_employee) == 1:
                    # only one so we assign it to rtn_val
                    rtn_val = varified_address_employee[0]
                else:
                    # more than one we look for records with dropshipping address
                    dropship_partners = partner.search([("type", "=", "drop_ship")])
                    if dropship_partners.ids:
                        # assign 1st dropshiping record found to partner_shiping_id
                        rtn_val = dropship_partners.ids[0]
                    else:
                        # no dropshiping record found assign 1st reord with bool == True
                        rtn_val = varified_address_employee[0]
                # writing the rtn_val in partner_shipping_id
                self.write({"partner_shipping_id": rtn_val})
