from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Fichier de log pour l'IDS
LOG_FILE = 'C:\\Users\\Windows\\ids_projet1\\flask_access.log'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Server'] = 'SecureServer'
        return response

    @app.before_request
    def log_request():
        """Ecrit chaque requete dans le fichier de log pour l'IDS"""
        ip = request.remote_addr
        ua = request.headers.get('User-Agent', '')
        path = request.full_path
        method = request.method
        log_line = f'{ip} - [{method}] {path} - UA: {ua}\n'
        try:
            with open(LOG_FILE, 'a') as f:
                f.write(log_line)
        except:
            pass

    from app.routes.auth import auth
    from app.routes.incidents import incidents
    app.register_blueprint(auth)
    app.register_blueprint(incidents)

    with app.app_context():
        db.create_all()

    return app