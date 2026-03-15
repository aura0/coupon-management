import json


def test_create_coupon(client):

    payload = {
        "type": "cart-wise",
        "details": {
            "threshold": 100,
            "discount": 10
        }
    }

    response = client.post(
        "/coupons",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "coupon_id" in data


def test_get_coupons(client):

    response = client.get("/coupons")

    assert response.status_code == 200


def test_apply_coupon(client):

    payload = {
        "type": "cart-wise",
        "details": {
            "threshold": 100,
            "discount": 10
        }
    }

    create = client.post(
        "/coupons",
        data=json.dumps(payload),
        content_type="application/json"
    )

    coupon_id = create.get_json()["coupon_id"]

    cart = {
        "cart": {
            "items": [
                {"product_id": 1, "quantity": 2, "price": 60}
            ]
        }
    }

    response = client.post(
        f"/apply-coupon/{coupon_id}",
        data=json.dumps(cart),
        content_type="application/json"
    )

    assert response.status_code == 200