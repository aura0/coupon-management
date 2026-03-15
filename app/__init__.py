from flask import Flask
from app.config import Config
from app.extensions import db ,ma
from app.errors import register_error_handlers

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    register_error_handlers(app)

    from app.routes.coupon_routes import coupon_bp
    app.register_blueprint(coupon_bp)

    with app.app_context():
        db.create_all()

    return app

