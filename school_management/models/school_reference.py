import random
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolReference(models.Model):
    _name = "school.reference"
    _description = "school reference contacts"
    _rec_name = "reference_name"

    reference_name = fields.Char(string="Referral Name", required=True)
    reference_phone = fields.Char(string="Referral Phone", required=True)
    discount_amount = fields.Char(string="Discount", required=True)
    reference_promo = fields.Char(string="Promo Code", store=True)

    @api.constrains("reference_name")
    def validate_reference_name(self):
        """using re to validate the name has no numbers in it #T00336"""
        excluded_char = re.findall(r"[0-9]+", self.reference_name)
        if excluded_char:
            raise ValidationError(_("Numbers not allowed in name"))

    @api.model
    def create(self, vals):
        """inhariting create method to make a randomly generated promo code from
        the promo_code function #T00336"""
        legal_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        final_code = ""
        # generating a random string which has 13 chars
        for _next_element in range(0, 13):
            next_char = random.randint(0, len(legal_chars) - 1)
            final_code += legal_chars[next_char]
        # the random code generated above is now put in the reference_promo field
        vals["reference_promo"] = final_code
        return super(SchoolReference, self).create(vals)
