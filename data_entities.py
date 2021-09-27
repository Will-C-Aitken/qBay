from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime   # Need for fields that include times
from sqlalchemy import ForeignKey  # Need for relationships between tables

# For now instantiate the app in this file, but will later migrate to using an
# application factory
app = Flask(__name__)

# Used to set location, whether remote or local, of database and type. The
# three slashes denote relative to the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Connect the database with the app
db = SQLAlchemy(app)

# Added in to suppress warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


'''
User database class that extends the database model class by default. Will be
converted to SQL statements by SQLAlchemy

Attributes:
    user_id - Unique user identifier
    username - Unique username
    email - User's email, must be unique
    password - For now store password as plaintext. Will need to update for
    security
    Balance - User's account balance in CAD
'''


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    balance = db.Column(db.Float)
    def __repr__(self):
        return '<User %r>' % self.username


'''
    class Product attributes:
    productID - Product identifier
    name - Name/title of the product
    seller - Name of seller
    price - Price of the item
    description - Description of the product
    size - Size of the product (e.g. S, L, OneSize, ...)
    category - Category of item (e.g. clothes, electronics, ...)
    img - Product image
    quantity - Number of items being sold
'''


class Product(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(40), nulltable=False)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name


"""
    An implementation of the Review class for Qbay.
    Review attributes:
    id - the unique id for each reivew
    author_id - the id of the author (of class User) for the review
    product_id - the id of the product (of class Product) for the reive
    rating - the rating (and int) of the product
    feedback - Text feedback on the product
    time - the time that the review was posted
"""


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)     # boundaries on rating value will be added later
    feedback = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<Review id: %r>" % self.id

