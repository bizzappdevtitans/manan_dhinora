{
    "name": "Product Seller",
    "summary": """A grouped view of sale, purchase, invoice based on the seller""",
    "author": "BizzAppDev Systems PVT. LTD.",
    "website": "http://www.bizzappdev.com",
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "sale_management",
        "purchase",
    ],
    "data": [
        "views/product_product_view.xml",
        "views/sale_report_view.xml",
        "views/purchase_report_view.xml",
        "views/account_invoice_report_view.xml",
    ],
}
