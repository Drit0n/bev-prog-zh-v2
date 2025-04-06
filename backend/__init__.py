from flask import Flask

def create_app():
    # Hier wird der Template-Ordner auf '../frontend' gesetzt,
    # da sich der Ordner "frontend" eine Ebene oberhalb von "backend" befindet.
    app = Flask(__name__, template_folder='../frontend')
    
    # Blueprints registrieren (z.B. aus routes.py)
    from backend.routes import bp
    app.register_blueprint(bp)
    
    return app
