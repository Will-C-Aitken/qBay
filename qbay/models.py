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


def update_user(email, password, update_params):
    '''
    Update a user

    Parameters:
        email (string):    user email
        password (string): user password
        update_params:   Hash table of entries to update

    Returns:
       True if update succeeded otherwise False
    '''
    # check if user creds can be authed by db
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return False

    # not all parameters can be updated
    allowed_params = {'shipping_address', 'postal_code', 'username'}
    for param in update_params:
        if param not in allowed_params:
            return False

    # validate the update parameters
    if 'shipping_address' in update_params:
        if not check_address(update_params['shipping_address']):
            return False
    if 'postal_code' in update_params:
        if not check_postal_code(update_params['postal_code']):
            return False
    if 'username' in update_params:
        if not check_username(update_params['username']):
            return False

    # update parameters
    if 'shipping_address' in update_params:
        user.shipping_address = update_params['shipping_address']
    if 'postal_code' in update_params:
        user.postal_code = update_params['postal_code']
    if 'username' in update_params:
        user.username = update_params['username']
    # actually save the user object
    db.session.commit()

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
    # Note that the date is included as a default parameter in the
    # create_product function.This is useful for testing, but should
    # not be available to users in the front-end (i.e. users should
    # not be able to input the date when the product is created
    # - it should be done automatically.

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


def update_product(title, price, seller_email, update_params):
    '''
    Update a product

    Parameters:
        title (string):     product title
        price (float):      product price
        seller_email (string):  email of seller
        update_params:   Hash table of entries to update

    Returns:
       True if update succeeded otherwise False
    '''

    # Current time
    last_modified_date = datetime.date.today()

    # Search for current product to be updated
    current_product = (Product.query.filter_by
                       (title=title, seller_email=seller_email).first())
    # Check if product exists
    if current_product is None:
        return False

    # ------ Validate that all attributes follow the requirements ----
    # Not all parameters can be updated
    allowed_params = {'description', 'title', 'price'}
    for param in update_params:
        if param not in allowed_params:
            return False    

    # Check that title format is correct
    if 'title' in update_params:
        if not check_title(update_params['title']):
            return False

    # Check that the description is of the correct length
    if 'description' in update_params:
        if not check_description(update_params['description'], title):
            return False

    # Check that price is within the allowed
    # range and can only be increased.
    if 'price' in update_params:
        if not check_price(update_params['price']):
            return False
        elif price > update_params['price']:
            return False

    # Check if date is within the allowed range.
    if not check_date(last_modified_date):
        return False

    # ---- Update attributes ----
    if 'title' in update_params:
        current_product.title = update_params['title']

    if 'description' in update_params:
        current_product.description = update_params['description']

    if 'price' in update_params:
        current_product.price = update_params['price']

    current_product.last_modified_date = last_modified_date

    # actually save the user object
    db.session.commit()

    return True


def order(prod_title, seller_email, buyer_email, date=datetime.date.today()):
    '''
    Order an available product. Products that have already been purchased will
    not appear when available products are listed for a user.

    Parameters:
        prod_title (string):           the products title
        seller_email (string):         the sellers email
        buyer_email (string):          the buyers email
        date (datetime) default - now: time of order

    Returns:
       True if order placement succeeded otherwise False
    '''

    # get product they want to order
    product = Product.query.filter_by(title=prod_title, 
                                      seller_email=seller_email).first()

    # Check if product exists
    if product is None:
        return False

    # get buyers email, they will aready be logged in so no need to check that
    # they exist
    buyer = User.query.filter_by(email=buyer_email).first()

    # ensure user does not by own product
    if buyer.email == product.seller_email:
        return False

    # ensure buyer has sufficient funds
    if buyer.balance < product.price:
        return False

    # Check that date of orider is within the allowed range. Used same range as
    # product creation
    if not check_date(date):
        return False

    # Create transaction
    trans = Transaction(buyer_email=buyer.email, 
                        product_id_num=product.id_num,
                        date=date, price=product.price)

    db.session.add(trans)

    # Update balances
    new_buyer_balance = buyer.balance - product.price
    buyer.balance = new_buyer_balance

    seller = User.query.filter_by(email=product.seller_email).first()
    new_seller_balance = seller.balance + product.price
    seller.balance = new_seller_balance

    # commit all chances to db
    db.session.commit()

    return True


def get_avail_products():
    '''
    Get list of non-bought products

    Returns:
        list of Products
    '''

    products = Product.query.all()

    # Exclude bought products
    filtered_products = []
    for p in products:
        trans = Transaction.query.filter_by(product_id_num=p.id_num).first()
        if trans is None:
            filtered_products.append(p)

    return filtered_products


def get_sold_products(seller_email):
    '''
    Get list of products sold by provided email

    Parameters:
        seller_email (string): the sellers email

    Returns:
        list of Products
    '''

    products = Product.query.filter_by(seller_email=seller_email).all()

    # Include only bought products
    filtered_products = []
    for p in products:
        trans = Transaction.query.filter_by(product_id_num=p.id_num).first()

        if trans is not None:
            filtered_products.append(p)

    return filtered_products


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


def check_address(addr):
    '''
    Verify that address conforms to requirements, i.e. alpha numeric
    non-empty string
    Parameters:
        username (string):    user address

    Returns:
        True if the address is valid, otherwise False
    '''
    return len(addr) > 0 and bool(re.match(r'[0-9a-zA-Z\s]+$', addr))


def check_postal_code(ps_code):
    '''
    Verify that postal code conforms to requirements, i.e. valid
    Canadian postalcode
    Parameters:
        username (string):    user postal code

    Returns:
        True if the postal is valid, otherwise False
    '''
    regex = r'[ABCEGHJ-NPRSTVXY][0-9][ABCEGHJ-NPRSTV-Z]'\
            r'\s[0-9][ABCEGHJ-NPRSTV-Z][0-9]'
    m = re.match(regex, ps_code)
    return m is not None


def check_title(title):
    """
    Verifies that the title is alphanumeric, lacks leading and trailing spaces,
    and is within thespecified length (<80 characters)

    :param title: the title to be checked
    :return: True if title meets criteria, False otherwise
    """
    # iterate over string and return False if any character
    # is neither alphanumeric nor a space
    for char in title:
        if (not char.isalnum()) and (not char.isspace()):
            return False
    # Could just use strip here, but I'm following the project
    # guidelines as written
    if title.startswith(" ") or title.endswith(" "):
        return False
    if len(title) > 80:
        return False
    return True


def check_description(description, title):
    """
    Verifies that the description is within the specified bounds
    (20 < x < 20000) and that the description is longer than the
    inputted title.

    :param description: product description
    :param title: product title
    :return: True if the description meets the requirements,
             False otherwise
    """
    if len(description) < 20 or len(description) > 2000:
        return False
    elif len(description) <= len(title):
        return False
    else:
        return True


def check_price(price):
    """
    Verifies that the given price is within the specified
    range (10.0 < x < 10000.0)

    :param price: a product's price
    :return: True if the price meets the requirements,
             False otherwise
    """
    if price < 10.0 or price > 10000.0:
        return False
    else:
        return True


def check_date(date):
    """
    Verifies that the given date is within the allowed
    range (2021-01-02 < x < 2025-01-02)

    :param date: a date (when product was created or last changed)
    :return: True if the date is within the allowed range,
             False otherwise
    """
    too_early = datetime.date(2021, 1, 2)
    too_late = datetime.date(2025, 1, 2)
    if date <= too_early or date >= too_late:
        return False
    else:
        return True


def check_seller(seller_email):
    """
    Verifies that the given email is attached to a User
    object in the database

    :param seller_email: an email (of the product's seller)
    :return: True if the email corresponds to an existing user,
            False otherwise
    """
    existing_seller = User.query.filter_by(email=seller_email).all()
    # Note that this rules out the possibility of an empty seller_email,
    # as it is impossible to create a user with an empty/invalid email.
    if not existing_seller:
        return False
    else:
        return True


def check_uniqueness(title, seller_email):
    """
    Verifies that the title is not already possessed by another
    product belonging to the seller. We assume that this requirement applies
    strictly to the products owned by the seller in question (so two
    *different* sellers could still have products with the same name)

    :param title: a product title
    :param seller_email: the seller's email
    :return: True if the title is not already possessed by a product
             of the seller, or False otherwise
    """
    already_exists = Product.query.filter_by(title=title,
                                             seller_email=seller_email).all()
    if already_exists:
        return False
    else:
        return True

