from app.extensions import db
from sqlalchemy.dialects.sqlite import JSON

class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    details = db.Column(JSON, nullable=False)