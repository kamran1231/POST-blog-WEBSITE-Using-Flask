
from . import db
from flask_login import UserMixin
from datetime import datetime



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    blog_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    author = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    pub_date = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.now())


    def __str__(self):
        return '<Blog %r>' % self.title