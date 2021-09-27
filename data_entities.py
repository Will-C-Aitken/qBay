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


# User database class that extends the database model class by default. Will be
# converted to SQL statements by SQLAlchemy
class User(db.Model):
    # Identification unique to each user. Will act as the primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # For now store password as plaintext. Will need to update for security in
    # the future
    password = db.Column(db.String(30), nullable=False)
    # Balance in dollars of the user. NULL signifies a balance of $0.00
    balance = db.Column(db.Float)

    # For now set the representation of a user as their username
    def __repr__(self):
        return '<User %r>' % self.username
