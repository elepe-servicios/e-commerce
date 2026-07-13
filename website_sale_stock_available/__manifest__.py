# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Stock Available",
    "summary": "Display 'Available to promise' in shop online instead "
    "of 'Free To Use Quantity'",
    "version": "19.0.1.0.3",
    "category": "Website",
    "website": "https://github.com/OCA/e-commerce",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "stock_available",
        "website_sale_stock",
    ],
    "data": [
        "views/website_sale_stock_guard.xml",
    ],
    "assets": {
        # Ensure this patch is loaded after website_sale_stock's own patch.
        "web.assets_frontend_lazy": [
            (
                "after",
                "website_sale_stock/static/src/js/variant_mixin.js",
                "website_sale_stock_available/static/src/js/website_sale_stock_available.js",
            ),
        ],
    },
    "installable": True,
}
