from qbay import app
from flask_sqlalchemy import SQLAlchemy
import datetime
import re

'''
This file defines data models and related business logics
'''


# Connect the database with the app
db = SQLAlchemy(app)


class User(db.Model):
    '''
    User class that extends the database model class by default. Will be
    converted to SQL statements by SQLAlchemy

    Attributes:
        email (string)
        username (string)
        password (string)
        shipping_address (string)
        postal_code (string) stored in the format _#_#_# where _ denotes 
         letters and # denotes numbers
        balance (float) account balance in CAD
    '''

    email = db.Column(db.String(120), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    # Consider implementing secure hashing. Not a requirement for now
    password = db.Column(db.String(120), nullable=False)

    shipping_address = (db.String(200))
    postal_code = (db.String(6))

    balance = db.Column(db.Float)

    # one-to-many relationship with product
    products = db.relationship('Product', backref='user', lazy=True)

    # one-to-many relationship with transaction
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    # one-to-many relationship with review
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Product(db.Model):
    '''
    Product class that extends the database model class by default. Will be
    converted to SQL statements by SQLAlchemy

    Attributes:
        id_num (integer) product identifier
        title (string) 
        description (text) 
        price (float) in CAD
        last_modified_date (datetime)
        seller_email (string) 
    '''

    id_num = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)
    last_modified_date = db.Column(db.DateTime, nullable=False) 

    # foreign key to user table
    seller_email = db.Column(db.String(80), db.ForeignKey('user.email'), 
                             nullable=False)

    # one-to-many relationship with transaction
    transactions = db.relationship('Transaction', backref='product', lazy=True)

    # stretch goals:
    # size = db.Column(db.String(20), nullable=False)
    # category = db.Column(db.String(40), nulltable=False)
    # img = db.Column(db.String(20), nullable=False, default='default.jpg')
    # quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.title


class Transaction(db.Model):
    '''
    Transaction class that extends the database model class by default. Will be
    converted to SQL statements by SQLAlchemy

    Attributes:
        id_num (integer) transaction identifier
        buyer_email (string) 
        product_id_num (integer) 
        date (datetime) date of purchase
        price (float) in CAD
    '''

    id_num = db.Column(db.Integer, primary_key=True)

    # foreign key to user table
    buyer_email = db.Column(db.String(80), db.ForeignKey('user.email'),
                            nullable=False)

    # foreign key to product table
    product_id_num = db.Column(db.Integer, db.ForeignKey('product.id_num'),
                               nullable=False)

    date = db.Column(db.DateTime, default=datetime.datetime.now())
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Transaction %r>' % self.id_num


class Review(db.Model):
    '''
    Review class that extends the database model class by default. Will be
    converted to SQL statements by SQLAlchemy

    Attributes:
        id_num (integer) review identifier
        seller_email (string) reviews apply to the seller not the product
        rating (integer) scale to be defined
        feedback (text) body of review
        date (datetime) date of review
    '''
    id_num = db.Column(db.Integer, primary_key=True)

    # foreign key to user table
    seller_email = db.Column(db.String(80), db.ForeignKey('user.email'),
                             nullable=False)

    rating = db.Column(db.Integer, nullable=False)     
    feedback = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return "<Review %r>" % self.id_num


# create all tables
db.create_all()


def register(name, email, password):
    '''
    Register a new user

    Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password

    Returns:
       True if registration succeeded otherwise False
    '''
    # check that both username and password are not empty
    if (not email) or (not password):
        return False

    # check that email format is correct
    if not check_email(email):
        return False

    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True

def check_email(email):
    '''
    Verify that email conforms to RFC 5322 (with a few extra constraints, 
    each noted, for simplicity)

    Parameters:
        email (string):    user email

    Returns:
        True if the email is valid, otherwise False
    '''
    
    # assuming unquoted local part of address, refusing dots in any part of
    # the local name, and refusing hyphens in the domain.
    email_regex = (r'\b[A-Za-z0-9!#$&\'*+\-/=?^_`{|}~]{1,64}@'
                   r'([A-Za-z0-9]+\.)+[A-Za-z0-9]+\b')

    if re.fullmatch(email_regex, email):
        return True
    else:
        return False


def login(email, password):
    '''
    Check login information

    Parameters:
        email (string):    user email
        password (string): user password

    Returns:
        The user object if login succeeded otherwise None
    '''
    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]

#def update_user(email, username=None, shipping_address=None, postal_code=None):
# return True if successful, and False otherwise


