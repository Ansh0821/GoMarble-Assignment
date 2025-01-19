from flask import Flask
from app.routes import review_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(review_routes)  # Register your routes blueprint
    return app
