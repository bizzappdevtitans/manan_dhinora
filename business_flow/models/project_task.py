from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    # delcaring a field on project.task to get the value passed from SO #T00422
    project_task_description = fields.Text(string="Task Description")
