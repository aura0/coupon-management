from .base_strategy import CouponStrategy


class BxGyStrategy(CouponStrategy):

    def calculate(self, cart, details):

        buy = {p["product_id"]: p["quantity"] for p in details["buy_products"]}
        get = {p["product_id"]: p["quantity"] for p in details["get_products"]}
        limit = details.get("repition_limit", 1)

        cart_qty = {item["product_id"]: item["quantity"] for item in cart["items"]}

        possible = float("inf")

        # calculate how many times coupon can apply
        for pid, qty in buy.items():
            if pid in cart_qty:
                possible = min(possible, cart_qty[pid] // qty)
            else:
                possible = 0

        applications = min(possible, limit)

        if applications == 0:
            return 0, cart["items"]

        discount = 0
        updated_items = []

        for item in cart["items"]:

            item_copy = item.copy()
            item_copy["total_discount"] = 0

            if item["product_id"] in get:

                free_qty = get[item["product_id"]] * applications

                discount_amount = free_qty * item["price"]

                item_copy["total_discount"] = discount_amount

                discount += discount_amount

            updated_items.append(item_copy)

        return discount, updated_items
    
