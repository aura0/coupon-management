from app.strategies.cart_wise_strategy import CartWiseStrategy
from app.strategies.product_wise_strategy import ProductWiseStrategy
from app.strategies.bxgy_strategy import BxGyStrategy


def test_cart_wise_strategy():

    strategy = CartWiseStrategy()

    cart = {
        "items": [
            {"product_id": 1, "quantity": 2, "price": 60}
        ]
    }

    details = {
        "threshold": 100,
        "discount": 10
    }

    discount, _ = strategy.calculate(cart, details)

    assert discount == 12


def test_product_wise_strategy():

    strategy = ProductWiseStrategy()

    cart = {
        "items": [
            {"product_id": 1, "quantity": 2, "price": 50}
        ]
    }

    details = {
        "product_id": 1,
        "discount": 20
    }

    discount, _ = strategy.calculate(cart, details)

    assert discount == 20


def test_bxgy_strategy():

    strategy = BxGyStrategy()

    cart = {
        "items": [
            {"product_id": 1, "quantity": 4, "price": 50},
            {"product_id": 3, "quantity": 2, "price": 25}
        ]
    }

    details = {
        "buy_products": [{"product_id": 1, "quantity": 2}],
        "get_products": [{"product_id": 3, "quantity": 1}],
        "repition_limit": 2
    }

    discount, _ = strategy.calculate(cart, details)

    assert discount == 50