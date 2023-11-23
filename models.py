import sqlalchemy
from flask_sqlalchemy import SQLAlchemy, model
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import Relationship

db = SQLAlchemy()

class users(UserMixin, db.Model):

    __tablename__ = 'users'
    __table_args__ = {'schema': 'art'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(120))
    pw = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    posts = db.Relationship('post', backref='post')
    about = db.Relationship('about', backref='about')

    def __init__(self, id: int, username: str, email: str, pw: str, is_active: bool, posts) -> None:
        super().__init__()
        self.id= id
        self.username = username
        self.email = email
        self.password = pw

        self.is_active = is_active
        self.posts = posts

    def get_id(self):
        return str(self.id)
    
class post(db.Model):

    __tablename__ = 'post'
    __table_args__ = {'schema': 'art'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('art.users.id'), nullable=False)

    user = db.relationship('users', back_populates='posts')

    def __init__(self, id: int, title: str, body: str, img_url: str, user_id: int) -> None:
        super().__init__()
        self.id = id
        self.title = title
        self.body = body
        self.img_url = img_url
        self.user_id = user_id

class about(db.Model):

    __tablename__ = 'about'
    __table_args__ = {'schema': 'art'}

    user_id  = db.Column(db.Integer, db.ForeignKey('art.users.id'), nullable=False, primary_key=True)
    body = db.Column(db.String, nullable=False)



    def __init__(self, user_id: int, body: str):
        super().__init__()
        self.user_id = user_id
        self.body = body


        





