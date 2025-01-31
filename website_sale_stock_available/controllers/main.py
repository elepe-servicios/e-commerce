# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.http import request, route

from odoo.addons.website_sale_stock.controllers.main import website_sale_controller


class WebsiteSale(website_sale_controller.WebsiteSale):
    @route(
        '/shop/payment/transaction/<int:order_id>', type='json', auth='public', website=True
    )
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        """Inject a context when potential or promised stock is set"""
        request.website = request.website.with_context(
            website_sale_stock_available=True
        )
        return super().shop_payment_transaction(order_id, access_token, **kwargs)
