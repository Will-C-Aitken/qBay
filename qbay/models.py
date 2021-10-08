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

    shipping_address = db.Column(db.String(200), default='')
    postal_code = db.Column(db.String(6), default='')

    balance = db.Column(db.Float, default=100.00)

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

    # check that password format is correct
    if not check_pass(password):
        return False

    # check that username format is correct
    if not check_username(name):
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


def check_pass(password):
    '''
    Verify that password conforms to requirements, i.e. is at least 6
    characters, at least one upper and one lower case letters, and at least one
    special character (one of [@$!%*?&])

    Parameters:
        password (string):    user password

    Returns:
        True if the password is valid, otherwise False
    '''
    
    # r'(at least one lower case)(at least one upper case)(at least one
    # special)total 6 or greater characters')
    password_regex = (r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])'
                      r'[a-zA-Z0-9@$!%*?&]{6,}$')

    if re.fullmatch(password_regex, password):
        return True
    else:
        return False


def check_username(username):
    '''
    Verify that username conforms to requirements, i.e. is longer than 2
    characters, less than 20 characters, alphanumeric-only, and neither
    beginnning or ending in spaces

    Parameters:
        username (string):    user username

    Returns:
        True if the username is valid, otherwise False
    '''
    
    # not space regexes at beginning and end count as one character so only
    # need 1-17 middle characters to be between (2, 20) exclusive
    username_regex = r'[a-zA-Z0-9][a-zA-Z0-9 ]{1,17}[a-zA-Z0-9]'

    if re.fullmatch(username_regex, username):
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


'''
def update_user(email, username=None, shipping_address=None, postal_code=None):
    return True if successful, and False otherwise
'''


def create_product(title,
                   description,
                   price,
                   seller_email,
                   date=datetime.date.today()):
    """
    Create a new product.

    :param title: product's title
    :param description: product's description
    :param price: product's price
    :param seller_email: email of seller
    :param date: the date of creation (default is set to current time)
    :return: True if product is successfully created, False otherwise
    """

    # Check that title format is correct
    if not check_title(title):
        return False

    # check that the description is of the correct length
    elif not check_description(description, title):
        return False

    # Check that price is within the allowed range
    elif not check_price(price):
        return False

    # Check that date of creation is within the allowed range
    elif not check_date(date):
        return False

    # check that seller_email is valid
    elif not check_seller(seller_email):
        return False

    # Check that the product's title has not already been used
    elif not check_uniqueness(title, seller_email):
        return False

    else:
        # create a new Product
        product = Product(title=title,
                          description=description,
                          price=price,
                          last_modified_date=date,
                          seller_email=seller_email)
        # add product to the current database session
        db.session.add(product)
        # save product object
        db.session.commit()
        return True


def check_title(title):
    """
    Verifies that the title is alphanumeric, lacks leading and trailing spaces,
    and is within thespecified length (<80 characters)

    :param title: the title to be checked
    :return: True if title meets criteria, False otherwise
    """
    # iterate over string and return False if any character is neither alphanumeric nor a space
    for char in title:
        if (not char.isalnum()) and (not char.isspace()):
            return False
    # Could just use strip here, but I'm following the project guidelines as written
    if title.startswith(" ") or title.endswith(" "):
        return False
    if len(title) > 80:
        return False
    return True


def check_description(description, title):
    """
    Verifies that the description is within the specified bounds (20 < x < 20000)
    and that the description is longer than the inputted title.

    :param description: product description
    :param title: product title
    :return: True if the description meets the requirements, False otherwise
    """
    if len(description) < 20 or len(description) > 2000:
        return False
    elif len(description) <= len(title):
        return False
    else:
        return True


def check_price(price):
    """
    Verifies that the given price is within the specified range (10 < x < 10000)

    :param price: a product's price
    :return: True if the price meets the requirements, False otherwise
    """
    if price < 10 or price > 10000:
        return False
    else:
        return True


def check_date(date):
    """
    Verifies that the given date is within the allowed range (2021-01-02 < x < 2025-01-02)

    :param date: a date (when product was created or last changed)
    :return: True if the date is within the allowed range, False otherwise
    """
    too_early = datetime.date(2021, 1, 2)
    too_late = datetime.date(2025, 1, 2)
    if date <= too_early or date >= too_late:
        return False
    else:
        return True


def check_seller(seller_email):
    """
    Verifies that the given email is attached to a User object in the database

    :param seller_email: an email (of the product's seller)
    :return: True if the email corresponds to an existing user, False otherwise
    """
    existing_seller = User.query.filter_by(email=seller_email).all()
    if not existing_seller:
        return False
    else:
        return True


def check_uniqueness(title, seller_email):
    """
    Verifies that the title is not already possessed by another product belonging to the seller.
    We assume that this requirement applies strictly to the products owned by the seller in question
    (so two *different* sellers could still have products with the same name)

    :param title: a product title
    :param seller_email: the seller's email
    :return: True if the title is novel (i.e., not already possessed by a product of the seller), or
    False otherwise
    """
    already_exists = Product.query.filter_by(title=title, seller_email=seller_email).all()
    if already_exists:
        return False
    else:
        return True
