from flask import jsonify, request , session
from main.db import mongo
import uuid
from datetime import datetime


class Message:
    def write(self):

        receiver = request.form.get('receiver', None)
        message = request.form.get('message', None)
        subject = request.form.get('subject')

# Message data validation
        if not receiver:
            return jsonify({"error": "A message must contain a receiver"}), 400
               
        if not subject:
            return jsonify({"error": "A message must contain a subject"}), 400

        receiver_user = mongo.db.users.find_one({'email': receiver})
        if not receiver_user:
            return jsonify({"error": "Received user could not be found"}), 400


# Added Sender_id and receiver_user because users sometimes change their email
# there-for any type of reference to the users should be done with the with unchangeable filed like primary key 
        
        message = {
            "_id": uuid.uuid4().hex,
            "sender": session['logged_in']['email'],
            "sender_id": session['logged_in']['_id'],
            "sender_name": session['logged_in']['name'],
            "receiver": receiver,
            "receiver_id": receiver_user['_id'],
            "receiver_name": receiver_user['name'],
            "message": message,
            "subject": subject,
            "creation_date": datetime.now(),
            'read': "No"
        }

        mongo.db.messages.insert_one(message)
        return jsonify("message was sent"), 200


    def all_messages(self):
        messages =mongo.db.messages.find({'receiver': session['logged_in']['_id']})
        response =[]
        for message in messages:
            response.append(message)
        if len(response) == 0:
            return jsonify("No messages found"), 200

        return jsonify({"messages": response}), 200

    def all_unread_messages(self):
        messages = mongo.db.messages.find({'receiver': session['logged_in']['_id'], 'read': "No"})
        response =[]

        for message in messages:
            response.append(message)

        if len(response) == 0:
            return jsonify({"error": "No messages found"}), 400

        return jsonify({"messages": response}), 200


    def read_message(self):
        response = mongo.db.messages.find_one({'receiver': session['logged_in']['_id'],'_id': request.args.get("id")})
        
        if response is None:
            return jsonify({"error": "The message does not exist"}), 400
        else: 
            mongo.db.messages.find_one_and_update({'receiver_id': session['logged_in']['_id'],'_id': request.args.get("id")},{ '$set':{'read': "Yes"}})
            return jsonify({"message": "The message was read"}), 200


    def delete_message(self):
        response = mongo.db.messages.find_one({'receiver_id': session['logged_in']['_id'],'_id': request.args.get("id")})
        if response is None:
            return jsonify({"error": "The message does not exist"}), 400
        else: 
            mongo.db.messages.delete_one({'receiver': session['logged_in']['_id'],'_id': request.args.get("id")})
            return jsonify("the message was deleted"), 200
    

    def conversation(self,id):
        # response = mongo.db.users.find_one({'_id': str(id)})
        if mongo.db.users.find_one({'_id': str(id)}) is None:
            return jsonify({"error": "The requested user does not exist"}), 400

# find all the messages with the session's user as the receiver and the requested user in the sender 
# OR the session's user as the sender and the requested user in the receiver
        messages = mongo.db.messages.find( { '$or': [{'receiver_id': session['logged_in']['_id'],'sender_id' : str(id)},{'sender_id': session['logged_in']['_id'],'receiver_id' : str(id)}]} ).sort('creation_date', -1)
        response =[]

        for message in messages:
            response.append(message)

        if len(response) == 0:
            return jsonify({"error": "You do not have a conversation with the requested user"}), 400
        
        return jsonify({"messages": response}), 200