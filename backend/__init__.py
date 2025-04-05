# backend/__init__.py
from flask import Flask
import os

def create_app():
    # Frontend folder explicitly given
    template_dir = os.path.abspath('frontend')

    app = Flask(__name__, template_folder=template_dir)

    # Import and register your routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app