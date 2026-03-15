# Coupons Management API for E-commerce Website

## Objective
Build a RESTful API to manage and apply different types of discount coupons:
- Cart-wise
- Product-wise
- BxGy (Buy X Get Y)

The system is **designed to be extensible**, so new coupon types can be added easily.

---

## Features Implemented
1. **Coupon Types**
   - Cart-wise (threshold-based discount)
   - Product-wise (discount on specific products)
   - BxGy with repetition limit (buy products from “buy” array → get products from “get” array)

2. **API Endpoints**
   - `POST /coupons` → Create new coupon
   - `GET /coupons` → Retrieve all coupons
   - `GET /coupons/{id}` → Retrieve coupon by ID
   - `PUT /coupons/{id}` → Update coupon
   - `DELETE /coupons/{id}` → Delete coupon
   - `POST /applicable-coupons` → List all applicable coupons for a cart
   - `POST /apply-coupon/{id}` → Apply a specific coupon to a cart

3. **Database**
   - SQLite used to store coupons
   - Flexible JSON `details` field for coupon rules

4. **Error Handling**
   - Invalid payload → 400
   - Coupon not found → 404
   - Missing cart → 400
   - Unsupported coupon type → safely ignored (discount = 0)
   - Safe discount calculation prevents negative totals

---

## Assumptions
- One coupon applied at a time (no stacking)
- Product IDs are unique integers
- Prices are positive floats
- Quantity is positive integer
- BxGy applies **only if minimum “buy” quantity is met**
- Discounts cannot exceed product price
- All coupons are global (no user-specific restrictions)
- Future coupon types can be added by extending `CouponEngine`

---

## Implemented Coupon Cases

### 1. Cart-wise Coupon
- **Example:** 10% off on carts > 100  
- **Condition:** Cart total > 100  
- **Payload:**
```json
{
  "type":"cart-wise",
  "details":{"threshold":100,"discount":10}
}