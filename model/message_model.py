from flask import jsonify, request , session
from main.db import mongo
import uuid
from datetime import datetime


class Message:
    def write(self):
        message = {
            "_id": uuid.uuid4().hex,
            "sender": session['logged_in']['email'],
            "receiver": request.form.get('receiver'),
            "message": request.form.get('message'),
            "subject": request.form.get('subject'),
            "creation_date": datetime.now(),
            'read': "No"
        }
        if mongo.db.users.find_one({'email': message['receiver']}):
            mongo.db.messages.insert_one(message)
            return jsonify("message was sent"), 200
        return jsonify({"error": "Received user could not be found"}), 400

    def all_messages(self):
        messages =mongo.db.messages.find({'receiver': session['logged_in']['email']})
        response =[]
        for message in messages:
            response.append(message)
        if len(response) == 0:
            return jsonify("No messages found"), 200

        return jsonify({"messages": response}), 200

    def all_unread_messages(self):
        messages =mongo.db.messages.find({'receiver': session['logged_in']['email'], 'read': "No"})
        response =[]
        for message in messages:
            response.append(message)
        if len(response) == 0:
            return jsonify({"error": "No messages found"}), 400

        return jsonify({"messages": response}), 200

    def read_message(self):
        response = mongo.db.messages.find_one({'receiver': session['logged_in']['email'],'_id': request.args.get("id")})
        if response is None:
            return jsonify({"error": "The message does not exist"}), 400
        else: 
            mongo.db.messages.find_one_and_update({'receiver': session['logged_in']['email'],'_id': request.args.get("id")},{ '$set':{'read': "Yes"}})
            return jsonify({"message": "The message was read"}), 200

    def delete_message(self):
        response = mongo.db.messages.find_one({'receiver': session['logged_in']['email'],'_id': request.args.get("id")})
        if response is None:
            return jsonify({"error": "The message does not exist"}), 400
        else: 
            mongo.db.messages.delete_one({'receiver': session['logged_in']['email'],'_id': request.args.get("id")})
            return jsonify("the message was deleted"), 200
