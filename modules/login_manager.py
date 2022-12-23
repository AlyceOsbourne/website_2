from flask import current_app, redirect, url_for, Blueprint, render_template, request
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

login_manager = LoginManager()
login_manager.login_view = 'login'

login_routes = Blueprint('login_routes', __name__)


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
    return Admin(current_app.config['ADMIN_USERNAME'], current_app.config['ADMIN_PASSWORD'])


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@login_routes.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == current_app.config['ADMIN_USERNAME'] and check_password_hash(
                current_app.config['ADMIN_PASSWORD'], password):
            if login_user(Admin(username, password)):
                return redirect(url_for('dashboard'))
        return redirect(url_for('login', failed = True))
    return render_template('screens/login.html')


@login_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
