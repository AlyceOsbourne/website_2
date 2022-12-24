import os
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.String(100), default = os.environ.get('ADMIN_USERNAME'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
