from flask import jsonify, request
import uuid

from flask.globals import session
from main.db import mongo
from passlib.hash import pbkdf2_sha256


class User:
    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        # Check for existing email address
        if mongo.db.users.find_one({'email': user['email']}):
            return jsonify({"error": "Email address already in use"}), 400
        if mongo.db.users.insert_one(user):
            return self.start_session(user)
            

        return jsonify({"error": "Signup failed"}), 400

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['logged_in'] = user
        return jsonify(user), 200
    
    def logout(self):
        session.clear()
        return jsonify("User loged-out"), 200

    def login(self):
        user = mongo.db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401 #401 unauthorise 


# class User2(db.Document):
#     email = db.StringField(primary_key=True, required=True)
#     password = db.ListField(db.StringField(), required=True)
#     name = db.ListField(db.StringField(), required=True)
    