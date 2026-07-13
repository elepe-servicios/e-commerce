/** @odoo-module **/
// Fix: VariantMixin._onChangeCombinationStock crashes with
//   "TypeError: Cannot read properties of null (reading 'append')"
// when a product template does not include the `.availability_messages`
// container that website_sale_stock expects.
//
// This patch is placed in web.assets_frontend_lazy in this module
// (which depends on website_sale_stock) so it runs AFTER
// website_sale_stock has applied its own patch to VariantMixin.
// Placing it in web.assets_frontend would be too early and
// website_sale_stock's patch would overwrite our guard.

import VariantMixin from "@website_sale/js/sale_variant_mixin";

// Idempotency guard: avoid double-wrapping if loaded twice.
if (!VariantMixin.__seycoStockGuardPatched__) {
    VariantMixin.__seycoStockGuardPatched__ = true;

    const _superOnChangeCombinationStock = VariantMixin._onChangeCombinationStock;

    VariantMixin._onChangeCombinationStock = function () {
        if (!_superOnChangeCombinationStock) {
            return;
        }

        const isParentLike = (v) =>
            v && (v.jquery || v.nodeType === 1 || typeof v.querySelector === "function");

        const parent = isParentLike(arguments[1])
            ? arguments[1]
            : isParentLike(arguments[0])
            ? arguments[0]
            : null;

        // If we cannot resolve a valid parent, do not delegate to stock code.
        // The upstream implementation assumes a valid container and can crash.
        if (!parent) {
            return;
        }

        const hasContainer = parent.jquery
            ? parent.find(".availability_messages").length > 0
            : !!parent.querySelector(".availability_messages");

        // No target container in this template -> skip stock message rendering.
        if (!hasContainer) {
            return;
        }

        try {
            return _superOnChangeCombinationStock.apply(this, arguments);
        } catch (e) {
            if (e instanceof TypeError && /append/i.test(String(e.message || ""))) {
                console.warn(
                    "[website_sale_stock_available] _onChangeCombinationStock skipped:",
                    e.message
                );
                return;
            }
            throw e;
        }
    };
}
