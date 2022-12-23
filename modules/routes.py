from flask import Blueprint, render_template
from flask_login import login_required

page_routes = Blueprint('page_routes', __name__)


@page_routes.route('/')
def index():
    return render_template('pages/index.html')


@page_routes.route('/about')
def about():
    return render_template('pages/about.html')


@page_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')
