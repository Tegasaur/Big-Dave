import flask
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Document):
    first_name = db.StringField( max_length = 50)
    last_name =  db.StringField( max_length = 50)
    email = db.StringField( max_length = 30, unique=True)
    password =  db.StringField( )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class Menu(db.Document):
    meal_name = db.StringField( max_length = 50)
    meal_price = db.DecimalField( precision = 2 )
    meal_description = db.StringField()
    meal_special = db.BooleanField()

class Parts(db.Document):
    part_name = db.StringField(max_length = 50)
    part_price = db.DecimalField(precision = 2)
    stock = db.IntField()
    image = db.ImageField()

class Cart(db.Document):
    user_email = db.StringField(max_length = 30)
    item_id = db.StringField(unique=True)

class Payment(db.Document):
    user_id = db.StringField()
    card_name = db.StringField()
    card_number = db.IntField(max_length = 16, min_length = 16)
    cvv = db.IntField(max_length = 3, mix_length = 3)
    expiry = db.DateTimeField(default=datetime.utcnow)
    zipcode = db.IntField(max_length = 5, mix_length = 5)

class Feedback(db.Document):
    name = db.StringField()
    email = db.StringField()
    subject = db.StringField()
    message = db.StringField()

