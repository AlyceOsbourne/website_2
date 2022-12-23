import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from app.ext import ext
from app.views import views

load_dotenv()

login_manager = LoginManager()
db = SQLAlchemy()

admin_username = os.environ.get('ADMIN_USERNAME') or 'admin'
admin_password = os.environ.get('ADMIN_PASSWORD') or 'admin'


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'change_me'
    app.config['ADMIN_USERNAME'] = admin_username
    app.config['ADMIN_PASSWORD'] = generate_password_hash(admin_password)
    app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL') or 'admin@site.com'
    app.config['GITHUB_PAGE'] = os.environ.get('GITHUB_PAGE') or 'github.com/username/repo'

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'info'

    from app.models import Post, Admin

    views(app)
    ext(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(_):
        return Admin(app.config['ADMIN_USERNAME'], app.config['ADMIN_PASSWORD'])

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('login'))

    return app
