from messages.view import messages
from auth.view import auth
from flask import Flask
from main.db import mongo
from datetime import timedelta


def create_app():

    app = Flask(__name__)
    app.permanent_session_lifetime = timedelta(seconds=60)
    app.config.from_object('config')
    mongo.init_app(app)

    app.register_blueprint(messages)
    app.register_blueprint(auth)
    
    return app