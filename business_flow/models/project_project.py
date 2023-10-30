from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "project.project"

    # delcaring a field on project.project to get the value passed from SO #T00422
    project_description = fields.Text(string="Project - Sale Description")
