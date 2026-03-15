from .base_strategy import CouponStrategy

class CartWiseStrategy(CouponStrategy):

    def calculate(self, cart, details):
        total = sum(item["price"] * item["quantity"] for item in cart["items"])

        if total >= details["threshold"]:
            discount = total * details["discount"] / 100
            return discount, cart["items"]

        return 0, cart["items"]