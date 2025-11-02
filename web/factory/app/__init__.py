import os
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import DevConfig, ProdConfig

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=DevConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # CLI to create admin users
    from app.auth.cli import init_auth_commands
    init_auth_commands(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # If running in development mode, turn on debug mode
    if app.config['DEBUG']:
        app.debug = True

    return app

from app import models
