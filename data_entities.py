from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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

