from app.models.coupon import Coupon
from app.extensions import db
from app.services.coupon_engine import CouponEngine

class CouponService:

    @staticmethod
    def create(data):
        coupon = Coupon(type=data["type"], details=data["details"])
        db.session.add(coupon)
        db.session.commit()
        return coupon

    @staticmethod
    def apply_coupon(coupon_id, cart):
        from app.extensions import db
        
        coupon = db.session.get(Coupon, coupon_id)
        if not coupon:
            raise Exception("Coupon not found")

        return CouponEngine.apply(coupon, cart)
    

    # -------------------------
    # READ ALL
    # -------------------------
    @staticmethod
    def get_all():
        return Coupon.query.all()

    # -------------------------
    # READ BY ID
    # -------------------------
    @staticmethod
    def get_by_id(coupon_id):
        return Coupon.query.get(coupon_id)

    # -------------------------
    # UPDATE
    # -------------------------
    @staticmethod
    def update_coupon(coupon_id, data):

        coupon = Coupon.query.get(coupon_id)

        if not coupon:
            return None

        coupon.type = data.get("type", coupon.type)
        coupon.details = data.get("details", coupon.details)

        db.session.commit()
        return coupon

    # -------------------------
    # DELETE
    # -------------------------
    @staticmethod
    def delete_coupon(coupon_id):

        coupon = Coupon.query.get(coupon_id)

        if not coupon:
            return False

        db.session.delete(coupon)
        db.session.commit()
        return True