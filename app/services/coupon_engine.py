from app.strategies.cart_wise_strategy import CartWiseStrategy
from app.strategies.product_wise_strategy import ProductWiseStrategy
from app.strategies.bxgy_strategy import BxGyStrategy

class CouponEngine:

    strategies = {
        "cart-wise": CartWiseStrategy(),
        "product-wise": ProductWiseStrategy(),
        "bxgy": BxGyStrategy()
    }

    @staticmethod
    def apply(coupon, cart):

        strategy = CouponEngine.strategies.get(coupon.type)

        if not strategy:
            raise ValueError("Unsupported coupon type")

        return strategy.calculate(cart, coupon.details)
    @staticmethod
    def get_applicable_coupons(coupons, cart):
        """
        Returns all coupons that give discount for given cart.
        """

        applicable = []

        for coupon in coupons:

            # Use existing calculate method
            discount, _ = CouponEngine.calculate_discount(coupon, cart)

            if discount > 0:
                applicable.append({
                    "coupon_id": coupon.id,
                    "type": coupon.type,
                    "discount": discount
                })

        return applicable
    @staticmethod
    def calculate_discount(coupon, cart):
    
        strategy = CouponEngine.STRATEGY_MAP.get(coupon.type)
    
        if not strategy:
            return 0, cart["items"]
    
        return strategy.calculate(cart, coupon.details)