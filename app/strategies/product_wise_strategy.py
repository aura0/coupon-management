from .base_strategy import CouponStrategy

class ProductWiseStrategy(CouponStrategy):

    def calculate(self, cart, details):

        discount_total = 0
        updated_items = []

        for item in cart["items"]:
            item_copy = item.copy()

            if item["product_id"] == details["product_id"]:
                item_discount = (
                    item["price"] * item["quantity"]
                ) * details["discount"] / 100

                item_copy["total_discount"] = item_discount
                discount_total += item_discount
            else:
                item_copy["total_discount"] = 0

            updated_items.append(item_copy)

        return discount_total, updated_items