from flask import Flask, request
from config import Config
from extension import db, login_manager, bcrypt
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.doctor import doctor_bp
from routes.reception import reception_bp
from ids_engine import IDS

ids = IDS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
     db.create_all()
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # ids = IDS()
    app.ids = ids

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(doctor_bp)
    app.register_blueprint(reception_bp)

    # IDS middleware
    @app.before_request
    def monitor_request():
        # print("🔥 BEFORE REQUEST TRIGGERED")  # DEBUG


         result = app.ids.inspect_request(request)
         if result:
             return result
    
    
    @app.after_request
    def add_header(response):
     response.cache_control.no_store = True
     return response
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)