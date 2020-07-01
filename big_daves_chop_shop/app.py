from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db =  MongoEngine()
db.init_app(app)

from restaurant.routes import food
from connector.routes import conn
from bike_shop.routes import bike

app.register_blueprint(food,url_prefix='/' )
app.register_blueprint(conn,url_prefix='/')
app.register_blueprint(bike,url_prefix='/')