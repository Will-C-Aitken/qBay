ifrom flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

'''
    class Transaction:
      This class defines a 
    Transaction table definition:
      id - Transaction identifier
      user_id - id of the user buying the item
      sell_id - id of the user selling the item
      item_id - id of the item being bought
      time - time of purchase
      price - price of item
      shipping_address - where the item is being shipped
'''
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    time =  db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "{}: USER_ID:{} ITEM:{} PRICE:${.2f} SHIP_TO:{}".format(self.time, self.user_id, self.itel_id, self.price, self.shipping_address)
