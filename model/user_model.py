from flask import jsonify, request
import uuid

from flask.globals import session
from main.db import mongo
from passlib.hash import pbkdf2_sha256


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
            return self.start_session(user)
            

        return jsonify({"error": "Signup failed"}), 400
    
# Session for auth - better suited for this project

    def start_session(self, user):
        del user['password']
        session.permanent = True
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

    def all_users_admin(self):
        users =mongo.db.users.find()
        response =[]
        for user in users:
            response.append(user)
        if len(response) == 0:
            return jsonify("No users found"), 200

        return jsonify({"users": response}), 200
