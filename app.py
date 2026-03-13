from flask import Flask, request, jsonify
from database import db
from models import Coupon
from coupon_engine import apply_coupon

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coupons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables if not exist
with app.app_context():
    db.create_all()

# ---------------------------
# CRUD Endpoints for Coupons
# ---------------------------

@app.route("/coupons", methods=["POST"])
def create_coupon():
    """Create a new coupon"""
    data = request.json
    if not data or "type" not in data or "details" not in data:
        return jsonify({"error": "Invalid coupon payload"}), 400

    coupon = Coupon(type=data["type"], details=data["details"])
    db.session.add(coupon)
    db.session.commit()
    return jsonify({"message": "Coupon created", "coupon_id": coupon.id})


@app.route("/coupons", methods=["GET"])
def get_coupons():
    """Get all coupons"""
    coupons = Coupon.query.all()
    return jsonify([{"id": c.id, "type": c.type, "details": c.details} for c in coupons])


@app.route("/coupons/<int:id>", methods=["GET"])
def get_coupon(id):
    """Get coupon by ID"""
    coupon = Coupon.query.get(id)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    return jsonify({"id": coupon.id, "type": coupon.type, "details": coupon.details})


@app.route("/coupons/<int:id>", methods=["PUT"])
def update_coupon(id):
    """Update a coupon"""
    coupon = Coupon.query.get(id)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    coupon.type = data.get("type", coupon.type)
    coupon.details = data.get("details", coupon.details)
    db.session.commit()
    return jsonify({"message": "Coupon updated"})


@app.route("/coupons/<int:id>", methods=["DELETE"])
def delete_coupon(id):
    """Delete a coupon"""
    coupon = Coupon.query.get(id)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    db.session.delete(coupon)
    db.session.commit()
    return jsonify({"message": "Coupon deleted"})


# ---------------------------
# Apply Coupons
# ---------------------------

@app.route("/applicable-coupons", methods=["POST"])
def applicable_coupons():
    """Get all applicable coupons for a given cart"""
    data = request.json
    cart = data.get("cart")
    if not cart:
        return jsonify({"error": "Cart missing"}), 400

    coupons = Coupon.query.all()
    applicable = []

    for coupon in coupons:
        updated_cart, discount = apply_coupon(cart, coupon)
        if discount > 0:
            applicable.append({"coupon_id": coupon.id, "type": coupon.type, "discount": discount})

    return jsonify({"applicable_coupons": applicable})


@app.route("/apply-coupon/<int:id>", methods=["POST"])
def apply_coupon_endpoint(id):
    """Apply a specific coupon to the cart"""
    coupon = Coupon.query.get(id)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    data = request.json
    cart = data.get("cart")
    if not cart:
        return jsonify({"error": "Cart missing"}), 400

    updated_cart, discount = apply_coupon(cart, coupon)
    return jsonify({"updated_cart": updated_cart})


# ---------------------------
# Global Error Handler
# ---------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True ,host='0.0.0.0',port=5000)