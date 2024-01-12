{
    "name": "Import Customer",
    "summary": """
        Import new customers from XML files.""",
    "license": "LGPL-3",
    "author": "BizzAppDev Systems PVT. LTD.",
    "website": "http://www.bizzappdev.com",
    "version": "16.0.1.0.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/import_customer_view.xml",
        "views/res_partner_view.xml",
    ],
}
