import os

from werkzeug.security import generate_password_hash

from modules.blog import blog_routes
from modules.context_processors import context_processors
from modules.filters import filters
from modules.login_manager import login_manager, login_routes
from modules.modals import db
from modules.routes import page_routes
from dotenv import load_dotenv

load_dotenv("instance/.env")
app_environ_defaults = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite",
    "SECRET_KEY": "change_me",
    "ADMIN_USERNAME": "admin",
    "ADMIN_PASSWORD": generate_password_hash("admin"),
    "ADMIN_EMAIL": "admin@site.com",
    "GITHUB_PAGE": "github.com/username/repo",
    "DISCORD_INVITE": "discord.gg/invite",
    "CODEPEN_PAGE": "codepen.io/username",
}
blueprints = [login_routes, blog_routes, page_routes, filters, context_processors]


def setup_environment(app):
    for key, value in app_environ_defaults.items():
        app.config[key] = os.environ.get(key) or value


def register_blueprints(app):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def setup_app(app):
    with app.app_context():
        setup_environment(app)
        register_blueprints(app)
        login_manager.init_app(app)
        db.init_app(app)
        db.create_all()
    return app
