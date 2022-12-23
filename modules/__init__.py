import os

from werkzeug.security import generate_password_hash

from modules.blog import blog_routes
from modules.context_processors import context_processors
from modules.filters import filters
from modules.login_manager import login_manager, login_routes
from modules.modals import db
from modules.routes import page_routes
from dotenv import load_dotenv

load_dotenv()


def setup_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'change_me'
    app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME') or 'admin'
    app.config['ADMIN_PASSWORD'] = generate_password_hash(os.environ.get('ADMIN_PASSWORD') or 'admin')
    app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL') or 'admin@site.com'
    app.config['GITHUB_PAGE'] = os.environ.get('GITHUB_PAGE') or 'github.com/username/repo'
    app.config['DISCORD_INVITE'] = os.environ.get('DISCORD_INVITE') or 'discord.gg/invite'
    app.config['CODEPEN_PAGE'] = os.environ.get('CODEPEN_PAGE') or 'codepen.io/username'
    app.register_blueprint(login_routes)
    app.register_blueprint(blog_routes)
    app.register_blueprint(page_routes)
    app.register_blueprint(filters)
    app.register_blueprint(context_processors)
    with app.app_context():
        login_manager.init_app(app)
        db.init_app(app)
        db.create_all()

    return app
