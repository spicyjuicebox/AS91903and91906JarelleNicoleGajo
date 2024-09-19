from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# The models are linked with the tables in the database.
# User Model for the user table in the database.
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # The username and email must be unique.
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # Name of the default image.
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # When the user was created.
    # Has a relationship with posts, comments and likes.
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    orders = db.relationship('Order')

# Post Model for the post table in the database.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Title of the post.
    text = db.Column(db.Text, nullable=False) # Content of the post.
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # When the post was created.
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # Who created the post.
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

# Like Model for the like table in the database.
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # When the like was created.
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # Who liked the post.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

# Comment Model for the comment table in the database.
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False) # Content of the comment.
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) # When the comment was created.
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # Who created the comment.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_email = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    payment_method = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)