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
