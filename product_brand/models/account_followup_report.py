from odoo import _, models


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_brand_values(self, account_move):
        """New method to get the brand values in dict of all invoices of  account_move
        and making them comma seprated, using dict and list comprehension #T7127"""

        # using set() to avoid duplicats
        brands = set()
        for invoice_line in account_move.line_ids:
            if invoice_line.product_brand_id:
                brands.add(invoice_line.product_brand_id.name)
        return ", ".join(list(brands))

    def _get_followup_report_lines(self, options):
        """Inherited this method to add the rows for brands column
        using the method _get_brand_values() #T7127"""
        return_values = super(AccountFollowupReport, self)._get_followup_report_lines(
            options
        )
        # updated list of return values(with brands)
        updated_return_values = []
        for row in return_values:
            account_move = row.get("account_move")
            final_brand_string = ""
            if account_move:
                final_brand_string = self._get_brand_values(row.get("account_move"))
            # inserting the brand column in its respective row
            row.get("columns").insert(
                3,
                {
                    "name": final_brand_string,
                    "style": "text-align:center; white-space:normal;",
                    "template": "account_followup.cell_template_followup_report",
                },
            )
            updated_return_values.append(row)
        return updated_return_values

    def _get_followup_report_columns_name(self):
        """Inherited method to add the column 'Brands' after 'Origin' in
        table-header #T7127"""
        values = super(AccountFollowupReport, self)._get_followup_report_columns_name()
        values.insert(
            4, {"name": _("Brands"), "style": "text-align:center; white-space:nowrap;"}
        )
        return values
