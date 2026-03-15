from app.extensions import ma
from app.models.coupon import Coupon
from marshmallow import fields, validate


class CouponSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Coupon
        load_instance = True

    id = fields.Int(dump_only=True)

    type = fields.Str(
        required=True,
        validate=validate.OneOf(["cart-wise", "product-wise", "bxgy"])
    )

    details = fields.Dict(required=True)
    

# Create instances
coupon_schema = CouponSchema()
coupons_schema = CouponSchema(many=True)