from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialize extensions (they’ll be bound to our app later)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Login settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register Blueprints
    from app.routes.auth import auth
    from app.routes.pickups import pickups_bp
    from app.routes.complaints import complaints
    from app.routes.dashboard import dashboard
    from app.routes.tracking import tracking_bp
    from app.routes.admin import admin
    from app.routes.driver import driver_bp


    app.register_blueprint(auth)
    app.register_blueprint(pickups_bp)
    app.register_blueprint(complaints)
    app.register_blueprint(dashboard)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(admin)
    app.register_blueprint(driver_bp)

    return app
