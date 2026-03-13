def calculate_cart_wise(cart, details):
    total = sum(item['price'] * item['quantity'] for item in cart['items'])
    if total >= details.get("threshold", 0):
        discount = total * details.get("discount", 0) / 100
        return discount, cart['items']
    return 0, cart['items']


def calculate_product_wise(cart, details):
    discount_total = 0
    updated_items = []
    for item in cart['items']:
        item_discount = 0
        if item['product_id'] == details.get("product_id"):
            item_discount = item['price'] * item['quantity'] * details.get("discount", 0) / 100
        updated_item = item.copy()
        updated_item["total_discount"] = item_discount
        discount_total += item_discount
        updated_items.append(updated_item)
    return discount_total, updated_items


def calculate_bxgy(cart, details):
    """
    Buy X products from buy_products → get Y products from get_products free
    Handles repetition limit
    """
    buy_map = {p['product_id']: p['quantity'] for p in details.get("buy_products", [])}
    get_map = {p['product_id']: p['quantity'] for p in details.get("get_products", [])}
    repetition_limit = details.get("repition_limit", 1)

    # Count how many times coupon can be applied
    cart_count = {}
    for item in cart['items']:
        cart_count[item['product_id']] = item['quantity']

    # Determine how many full sets of "buy" products exist
    possible_applications = float('inf')
    for pid, qty_needed in buy_map.items():
        if pid in cart_count:
            possible_applications = min(possible_applications, cart_count[pid] // qty_needed)
        else:
            possible_applications = 0
    # Cap by repetition limit
    applications = min(possible_applications, repetition_limit)
    if applications == 0:
        return 0, cart['items']

    discount_total = 0
    updated_items = []
    # Apply discount for get products
    for item in cart['items']:
        updated_item = item.copy()
        free_qty = 0
        if item['product_id'] in get_map:
            free_qty = min(get_map[item['product_id']] * applications, item['quantity'])
            discount_amount = free_qty * item['price']
            updated_item["total_discount"] = discount_amount
            discount_total += discount_amount
        else:
            updated_item["total_discount"] = 0
        updated_items.append(updated_item)

    return discount_total, updated_items


def apply_coupon(cart, coupon):
    if coupon.type == "cart-wise":
        discount, items = calculate_cart_wise(cart, coupon.details)
        updated_cart = {"items": [{"product_id": i["product_id"], "quantity": i["quantity"], "price": i["price"], "total_discount": 0} for i in items]}
    elif coupon.type == "product-wise":
        discount, items = calculate_product_wise(cart, coupon.details)
        updated_cart = {"items": items}
    elif coupon.type == "bxgy":
        discount, items = calculate_bxgy(cart, coupon.details)
        updated_cart = {"items": items}
    else:
        discount = 0
        updated_cart = {"items": cart['items']}

    total_price = sum(i["price"] * i["quantity"] for i in updated_cart["items"])
    total_discount = sum(i.get("total_discount", 0) for i in updated_cart["items"])
    final_price = total_price - total_discount

    updated_cart["total_price"] = total_price
    updated_cart["total_discount"] = total_discount
    updated_cart["final_price"] = final_price

    return updated_cart, discount