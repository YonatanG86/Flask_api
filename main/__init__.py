from messages.view import messages
from auth.view import auth
from flask import Flask
from main.db import mongo


def create_app():

    app = Flask(__name__)
 
    app.config.from_object('config')
    mongo.init_app(app)

    app.register_blueprint(messages)
    app.register_blueprint(auth)
    
    return app