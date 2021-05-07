from flask import jsonify, request , session
from main.db import mongo
import uuid
from datetime import datetime


class Message:
    def write(self):

        receiver = request.form.get('receiver', None)
        message = request.form.get('message', None)
        subject = request.form.get('subject')

        if not receiver:
            return jsonify({"error": "A message must contain a receiver"}), 400
               
        if not subject:
            return jsonify({"error": "A message must contain a subject"}), 400

        message = {
            "_id": uuid.uuid4().hex,
            "sender": session['logged_in']['email'],
            "receiver": receiver,
            "message": message,
            "subject": subject,
            "creation_date": datetime.now,
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
        messages = mongo.db.messages.find({'receiver': session['logged_in']['email'], 'read': "No"})
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
    
    def conversation(self,id):
        response = mongo.db.users.find_one({'_id': str(id)})
    
        if response is None:
            return jsonify({"error": "The requested user does not exist"}), 400

        messages = mongo.db.messages.find( { '$or': [{'receiver': session['logged_in']['email'],'sender' : response['email']},{'sender': session['logged_in']['email'],'receiver' : response['email']}]} )
        response =[]

        for message in messages:
            response.append(message)

        if len(response) == 0:
            return jsonify({"error": "You do not have a conversation with the requested user"}), 400
        
        return jsonify({"messages": response}), 200