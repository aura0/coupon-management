from database import db
from sqlalchemy.dialects.sqlite import JSON

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # cart-wise, product-wise, bxgy
    details = db.Column(JSON, nullable=False)  # stores thresholds, product IDs, discount