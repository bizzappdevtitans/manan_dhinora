{
    "name": "fabrication_management",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "version": "15.0.0.0.0",
    "license": "LGPL-3",
    "depends": [
        "base",
        "sale_management",
        "purchase",
        "stock",
        "product",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/product_template_view.xml",
        "views/purchase_order_view.xml",
        "views/menu_fabrication_management.xml",
    ],
    "demo": ["data/fabrication_demo.xml"],
    "application": True,
    "installable": True,
}
