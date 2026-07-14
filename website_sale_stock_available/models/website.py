# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _get_product_page_proportions(self):
        """Add compatibility for 33% image width on older product templates.

        Some migrated/custom product templates still rely on this method to compute
        image/detail columns. Core Odoo 19 stores ``33_pc`` but does not map it in
        this method, which can return None and crash template indexing.
        """
        proportions = super()._get_product_page_proportions()
        if proportions:
            return proportions
        if self.product_page_image_width in ("33_pc", "33", "fixed_33"):
            return (4, 8)
        return proportions

