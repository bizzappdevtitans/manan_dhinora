{
    "name": "Product Seller",
    "summary": """a grouped view of sale, purchase, invoice based on the seller""",
    "author": "BizzAppDev",
    "website": "http://www.bizzappdev.com",
    "category": "Uncategorized",
    "version": "15.0.0.0.1",
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
