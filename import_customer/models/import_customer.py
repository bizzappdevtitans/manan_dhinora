import base64
from lxml import etree as ET
from odoo.exceptions import ValidationError
from odoo import _, api, fields, models


class ImportCustomer(models.Model):
    _name = "import.customer"
    _description = "Import Customer"
    _rec_name = "name"

    # Added new fields #T7156
    partner_ids = fields.One2many(
        "res.partner",
        "import_id",
        string="Partner",
    )
    created_partner = fields.Integer(
        compute="_compute_created_partner", string="Customers"
    )
    name = fields.Char(default=lambda self: ("New"), string="Number")
    partner_name = fields.Char(string="Name")
    import_file = fields.Binary(copy=False)
    import_file_name = fields.Char(string="File")

    @api.model_create_multi
    def create(self, vals_ls):
        """Inherited method to assign a sequence on create #T7156"""
        for vals in vals_ls:
            vals["name"] = self.env["ir.sequence"].next_by_code("import.customer")
            return super().create(vals)

    def import_customer(self):
        """New method will parse the uploaded xml file and create a new res_partner
        record based on it #T7156"""
        if ".xml" not in self.import_file_name:
            raise ValidationError(_("Please upload an XML file."))
        if not self.import_file:
            raise ValidationError(_("Please upload a file to import customers."))
        file_as_str = base64.b64decode(self.import_file)
        try:
            xml = ET.fromstring(file_as_str)
        # if the XML is missing root tags raise error. #T7156
        except ET.XMLSyntaxError:
            raise ValidationError(_("The uploded file is missing an XML tag."))
        customer_ls = [
            {child.tag: child.text for child in customer} for customer in xml
        ]
        # creating new res_partner records and storing their ids for
        # the smart button. #T7156
        partner_ids = [
            self.env["res.partner"]
            .create(
                {
                    "name": customer.get("CustomerName"),
                    "ref": customer.get("14"),
                    "vat": customer.get("CustomerVat"),
                    "phone": customer.get("CustomerPhone"),
                    "mobile": customer.get("CustomerMobile"),
                    "is_company": True,
                    "email": customer.get("CustomerEmail"),
                    "street": customer.get("CustomerStreet1"),
                    "street2": customer.get("CustomerStreet2"),
                    "zip": customer.get("CustomerZip"),
                    "city": customer.get("CustomerCity"),
                    "country_code": customer.get("CustomerCountry"),
                    "import_id": self.id,
                }
            )
            .id
            for customer in customer_ls
        ]
        return self.write({"partner_ids": [(6, 0, partner_ids)]})

    @api.depends("partner_ids")
    def _compute_created_partner(self):
        """New compute method to count the total number of customers imported #T7156"""
        for imported in self:
            imported.created_partner = len(imported.partner_ids.ids)

    def action_open_partners(self):
        """New method to call the record created by import_customer() using the
        smart button #T7156"""
        return {
            "name": "Imported Customers",
            "res_model": "res.partner",
            "domain": [("id", "in", self.partner_ids.ids)],
            "view_mode": "tree,form",
            "target": "current",
            "type": "ir.actions.act_window",
        }
