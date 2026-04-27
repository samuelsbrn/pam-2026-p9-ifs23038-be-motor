from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.models.motor import Motor
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.models.user import User
from app.routes.auth_routes import auth_bp
from app.routes.motor_routes import motor_bp
from app.routes.motivation_routes import motivation_bp
from app.services.auth_service import seed_default_user

def create_app():
    app = Flask(__name__)
    
    # enable cors
    CORS(app)

    # create tables
    Base.metadata.create_all(bind=engine)
    seed_default_user()

    # register blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(motivation_bp)
    app.register_blueprint(motor_bp)

    return app
