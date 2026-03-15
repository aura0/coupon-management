from flask import Blueprint, request, jsonify
from app.services.coupon_engine import CouponEngine
from app.services.coupon_service import CouponService

# Create Blueprint
coupon_bp = Blueprint("coupon_bp", __name__)


# ----------------------------
# Create Coupon
# ----------------------------
@coupon_bp.route("/coupons", methods=["POST"])
def create_coupon():

    data = request.get_json()

    if not data or "type" not in data or "details" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    coupon = CouponService.create(data)

    return jsonify({
        "message": "Coupon created",
        "coupon_id": coupon.id
    }), 201


# ----------------------------
# Get All Coupons
# ----------------------------
@coupon_bp.route("/coupons", methods=["GET"])
def get_coupons():

    coupons = CouponService.get_all()

    result = []

    for c in coupons:
        result.append({
            "id": c.id,
            "type": c.type,
            "details": c.details
        })

    return jsonify(result)


# ----------------------------
# Apply Coupon
# ----------------------------
@coupon_bp.route("/apply-coupon/<int:coupon_id>", methods=["POST"])
def apply_coupon(coupon_id):

    data = request.get_json()

    if not data or "cart" not in data:
        return jsonify({"error": "Cart missing"}), 400

    try:

        updated_cart, discount = CouponService.apply_coupon(
            coupon_id,
            data["cart"]
        )

        return jsonify({
            "discount": discount,
            "updated_cart": updated_cart
        })

    except Exception as e:

        return jsonify({"error": str(e)}), 400
    
@coupon_bp.route("/applicable-coupons", methods=["POST"])
def applicable_coupons():

    data = request.get_json()

    if not data or "cart" not in data:
        return {"error": "Cart is required"}, 400

    coupons = CouponService.get_all()

    applicable = CouponEngine.get_applicable_coupons(
        coupons,
        data["cart"]
    )

    return {"applicable_coupons": applicable}, 200


# UPDATE
@coupon_bp.route("/coupons/<int:coupon_id>", methods=["PUT"])
def update_coupon(coupon_id):

    data = request.get_json()

    if not data:
        return {"error": "Invalid input"}, 400

    coupon = CouponService.update_coupon(coupon_id, data)

    if not coupon:
        return {"error": "Coupon not found"}, 404

    return {"message": "Coupon updated successfully"}, 200


# DELETE
@coupon_bp.route("/coupons/<int:coupon_id>", methods=["DELETE"])
def delete_coupon(coupon_id):

    deleted = CouponService.delete_coupon(coupon_id)

    if not deleted:
        return {"error": "Coupon not found"}, 404

    return {"message": "Coupon deleted successfully"}, 200


@coupon_bp.route("/ping", methods=["GET"])
def ping():
    return {"message": "API working"}, 200