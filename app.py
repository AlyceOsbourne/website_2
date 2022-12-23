import os
import re
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from markdown import markdown
from markupsafe import Markup
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'change_me'
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME') or 'admin'
app.config['ADMIN_PASSWORD'] = generate_password_hash(os.environ.get('ADMIN_PASSWORD') or 'admin')
app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL') or 'admin@site.com'
app.config['GITHUB_PAGE'] = os.environ.get('GITHUB_PAGE') or 'github.com/username/repo'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.String(100), default = app.config['ADMIN_USERNAME'])

    def __init__(self, title, content):
        self.title = title
        self.content = content


with app.app_context():
    db.create_all()


class Admin(UserMixin):
    def __init__(self, username, password):
        self.id = 1
        self.username = username
        self.password = generate_password_hash(password, method = 'pbkdf2:sha256:1000', salt_length = 8)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'Admin ' + str(self.id)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(_):
    return Admin(app.config['ADMIN_USERNAME'], app.config['ADMIN_PASSWORD'])


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('pages/index.html')


@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('blog/blog.html', posts = posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    return render_template('blog/post.html', post = Post.query.get_or_404(post_id))


# CREATE POST
@app.route('/post/create', methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        db.session.add(Post(request.form['title'], request.form['content']))
        db.session.commit()
        post_id = Post.query.order_by(Post.date.desc()).first().id
        return redirect(url_for('post', post_id = post_id))
    return render_template('blog/create.html')


@app.route('/post/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post', post_id = post_id))
    return render_template('blog/update.html', post = post)


@app.route('/post/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog'))


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/contact')
def contact():
    return render_template('pages/contact.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == app.config['ADMIN_USERNAME'] and check_password_hash(app.config['ADMIN_PASSWORD'], password):
            if login_user(Admin(username, password)):
                return redirect(url_for('dashboard'))
        return redirect(url_for('login', failed = True))
    return render_template('screens/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# filter to render text as markdown, with syntax highlighting.
# add css for the highlighting to the highlighted.css file.
@app.template_filter('markdown')
def highlight_filter(s):
    pattern = re.compile(r'```(\w+)?\s*([\s\S]+?)\s*```')

    def repl(match):
        lang = match.group(1)
        code = match.group(2)
        if lang:
            return highlight(code, get_lexer_by_name(lang), HtmlFormatter())
        else:
            return highlight(code, get_lexer_by_name('text'), HtmlFormatter())

    formatted = pattern.sub(repl, s)
    return Markup(markdown(formatted))


if __name__ == '__main__':
    app.run(
            debug = True,
            host = '0.0.0.0',
            port = 5000,
    )
