from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# For now instantiate the app in this file, but will later migrate to using an
# application factory
app = Flask(__name__)

# Used to set location, whether remote or local, of database and type. The
# three slashes denote relative to the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Connect the database with the app
db = SQLAlchemy(app)


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

