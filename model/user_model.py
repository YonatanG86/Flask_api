from flask import jsonify, request
import uuid
import jwt
import datetime
from flask.globals import session
from main.db import mongo
from passlib.hash import pbkdf2_sha256

from model.token_model import encode_auth_token
class User:
    def signup(self):
        name = request.form.get('name')
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        
        if not email:
            return jsonify({"error": "Email is missing"}), 400
        if not password:
            return jsonify({"error": "Password is missing"}), 400
        
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "email": email,
            "password": password
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if mongo.db.users.find_one({'email': user['email']}):
            return jsonify({"error": "Email address already in use"}), 400
        if mongo.db.users.insert_one(user):
            auth_token = encode_auth_token(user[id])
            self.assertTrue(isinstance(auth_token, bytes))
            return self.start_session(user)
            

        return jsonify({"error": "Signup failed"}), 400
    
# session 
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
            "email": request.form.get('email')})
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        return jsonify({"error": "Invalid login credentials"}), 401 
