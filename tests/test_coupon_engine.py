from app.services.coupon_engine import CouponEngine


class MockCoupon:
    def __init__(self, type, details):
        self.type = type
        self.details = details


def test_cart_wise_engine():

    coupon = MockCoupon(
        "cart-wise",
        {"threshold": 100, "discount": 10}
    )

    cart = {
        "items": [
            {"product_id": 1, "quantity": 2, "price": 60}
        ]
    }

    discount, _ = CouponEngine.apply(coupon, cart)

    assert discount == 12