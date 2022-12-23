from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, admin_username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100), default=admin_username)

    def __init__(self, title, content):
        self.title = title
        self.content = content


class Admin(UserMixin):
    def __init__(self, username, password):
        self.id = 1
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256:1000', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'Admin ' + str(self.id)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True
