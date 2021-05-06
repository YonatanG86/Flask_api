from messages.view import messages
from auth.view import auth
from flask import Flask
from main.db import mongo
import urllib


def create_app():
    # mongo_uri = "mongodb+srv://"+ urllib.parse.quote_plus("YoniGR") +":" + urllib.parse.quote_plus("Tbhnkl1986") + "@cluster0.rub43.mongodb.net/user_list?retryWrites=true&w=majority"
    c = 'mongodb+srv://Admin:Admin12345678@cluster0.rub43.mongodb.net/user_list?retryWrites=true&w=majority'

    app = Flask(__name__)
    app.secret_key = 'just_for_a_test'
    app.config["MONGO_URI"] = c
    mongo.init_app(app)

    app.register_blueprint(messages)
    app.register_blueprint(auth)
    return app