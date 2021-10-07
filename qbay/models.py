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


def check_address(addr):
    #validates an address
    return len(addr) > 0 and addr.isalnum()

def check_postal_code(ps_code):
    #validates a postal code using regex
    regex = '[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z]\s\d[ABCEGHJ-NPRSTV-Z]\d'
    m = re.match(regex, ps_code)
    return m != None


def update(email, password, update_params):
    '''
    Update a user

    Parameters:
        email (string):    user email
        password (string): user password
        update_params:   Hash table of entries to update

    Returns:
       True if update succeeded otherwise False
    '''
    #check if user creds can be authed by db
    user = User.query.filter_by(email=email, password=password).first()
    if user == None:
        return False
    
    #validate the update parameters
    if 'shipping_address' in update_params:
        if not check_address(update_params['shipping_address']):
            return False
    if 'postal_code' in update_params:
        if not check_postal_code(update_postal_code['postal_code']):
            return False
    if 'username' in update_params:
        if not check_username(update_username['username']):
            return False

    #update parameters
    if 'shipping_address' in update_params:
        user.shipping_address=update_params['shipping_address']
    if 'postal_code' in update_params:
        user.postal_code=update_params['postal_code']
    if 'username' in update_params:
        user.username=update_params['username']
    db.commit()

    return True


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
