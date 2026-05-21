from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
DEMO_MODE = True
ADMIN_IP = "127.0.0.1"

login_manager.login_view = "auth.login"