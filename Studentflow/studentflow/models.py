from datetime import datetime
from studentflow import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): # class user
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # user_id
    username = db.Column(db.String(25), unique=True, nullable=False) # username, string =   20(max)
    email = db.Column(db.String(125), unique=True, nullable=False) # user email, string 120(max)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # image file
    password = db.Column(db.String(65), nullable=False) # user password, string 60(max)
    about = db.Column(db.String(100), nullable=False, default='nothing') # about you string 100 max
    phone = db.Column(db.String(15), nullable=True, default='000-000-0000') # user's phone, user don't have to write it, 12 charactors max
    posts = db.relationship('Post', backref='author', lazy=True) # user post, relationship, backref = author
    chats = db.relationship('Chat', backref='author', lazy=True) 
    feedbacks = db.relationship('Feedback', backref='author', lazy=True) 
    create_account = db.Column(db.DateTime, nullable=False, default=datetime.now) # the time user create account
    badges = db.Column(db.DateTime, nullable=False, default=datetime.now) # the time when user get their badges
 
class Post(db.Model): # class post 
    __bind_key__ = 'post'
    id = db.Column(db.Integer, primary_key=True) # post_id
    title = db.Column(db.String(80), nullable=False) # post_title = string 80(max)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now) # date_post by datetime
    content = db.Column(db.Text, nullable=False) # post_content = text, no maxium
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    tag = db.Column(db.String(50), nullable=False) # tag for post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user_id 
