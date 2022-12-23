from flask import Blueprint, current_app, url_for

from .modals import Post

context_processors = Blueprint('context_processors', __name__)


@context_processors.app_context_processor
def num_posts():
    return dict(num_posts = Post.query.count())


@context_processors.app_context_processor
def github_page():
    return dict(github_page = current_app.config['GITHUB_PAGE'])


@context_processors.app_context_processor
def codepen_page():
    return dict(codepen_page = current_app.config['CODEPEN_PAGE'])


@context_processors.app_context_processor
def admin_username():
    return dict(admin_username = current_app.config['ADMIN_USERNAME'])


@context_processors.app_context_processor
def admin_email():
    return dict(admin_email = current_app.config['ADMIN_EMAIL'])


@context_processors.app_context_processor
def most_recent_post():
    return dict(
            most_recent_post = url_for('blog_routes.post', post_id = Post.query.order_by(Post.date.desc()).first().id))


@context_processors.app_context_processor
def discord_invite():
    return dict(discord_invite = current_app.config['DISCORD_INVITE'])
