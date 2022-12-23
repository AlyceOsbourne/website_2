from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from .modals import db, Post

blog_routes = Blueprint('blog_routes', __name__)



@blog_routes.route('/blog')
def blog():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('pages/blog.html', posts = posts)


@blog_routes.route('/post/<int:post_id>')
def post(post_id):
    return render_template('blog/post.html', post = Post.query.get_or_404(post_id))


# CREATE POST
@blog_routes.route('/post/create', methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post = Post(request.form['title'], request.form['content'])
        if request.form['title'] and request.form['content']:
            db.session.add(post)
            db.session.commit()
            post_id = Post.query.order_by(Post.date.desc()).first().id
            return redirect(url_for('post', post_id = post_id))
        else:
            return render_template('blog/update.html', post = post, error = 'Title and content are required')
    return render_template('blog/create.html')


@blog_routes.route('/post/update/<int:post_id>', methods = ['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post', post_id = post_id))
    return render_template('blog/update.html', post = post)


@blog_routes.route('/post/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog'))

