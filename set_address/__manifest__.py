{
    'name': "set address",
    'description': "setting delivery address based on address validaity",
    'author': "[MAD]",
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management'],
    'data': [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],

    "installable": True,
    "application": True,
}
