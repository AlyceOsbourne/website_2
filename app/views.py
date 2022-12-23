from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash


def views(app):
    from app import db
    from app.models import Post, Admin

    @app.route('/')
    def index():
        return render_template('pages/index.html')

    @app.route('/blog')
    def blog():
        posts = Post.query.order_by(Post.date.desc()).all()
        return render_template('blog/blog.html', posts=posts)

    @app.route('/post/<int:post_id>')
    def post(post_id):
        return render_template('blog/post.html', post=Post.query.get_or_404(post_id))

    # CREATE POST
    @app.route('/post/create', methods=['GET', 'POST'])
    @login_required
    def create():
        if request.method == 'POST':
            db.session.add(Post(request.form['title'], request.form['content']))
            db.session.commit()
            post_id = Post.query.order_by(Post.date.desc()).first().id
            return redirect(url_for('post', post_id=post_id))
        return render_template('blog/create.html')

    @app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def update(post_id):
        post = Post.query.get_or_404(post_id)
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            return redirect(url_for('post', post_id=post_id))
        return render_template('blog/update.html', post=post)

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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == current_app.config['ADMIN_USERNAME'] and check_password_hash(current_app.config['ADMIN_PASSWORD'], password):
                if login_user(Admin(username, password)):
                    return redirect(url_for('dashboard'))
            return redirect(url_for('login', failed=True))
        return render_template('screens/login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
