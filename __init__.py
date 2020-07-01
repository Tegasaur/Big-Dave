from flask import Flask
from flask_mongoengine import MongoEngine
from big_dave_chop_shop.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db =  MongoEngine()
db.init_app(app)

from big_dave_chop_shop.restaurant.routes import food
from big_dave_chop_shop.connector.routes import conn
from big_dave_chop_shop.bike_shop.routes import bike

app.register_blueprint(food,url_prefix='/' )
app.register_blueprint(conn,url_prefix='/')
app.register_blueprint(bike,url_prefix='/')