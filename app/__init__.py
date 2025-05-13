import logging
import os
from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager
from app.utils.logger import setup_logger

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Setup logger
    setup_logger()
    
    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.challenges import challenges_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(challenges_bp, url_prefix='/challenges')
    
    # Log application startup
    app.logger.info('CyberSentinels CTF started')
    
    return app