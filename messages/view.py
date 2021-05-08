from flask import Blueprint
from model.message_model import Message
from utilities.utilities import login_required

messages = Blueprint('messages', __name__)

@messages.route('/message/write/', methods=['POST'])
@login_required
def write():
    return Message().write()

@messages.route('/message/all/')
@login_required
def all():
    return Message().all_messages()

@messages.route('/message/unread/')
@login_required
def allunread():
    return Message().all_unread_messages()

@messages.route('/message/read/<id>/',methods=['POST'])
@login_required
def messageread(id):
    return Message().read_message(id)

@messages.route('/message/delete/<id>/', methods=['DELETE'])
@login_required
def delete(id):
    return Message().delete_message(id)

@messages.route('/message/<id>/')
@login_required
def conversation(id):
    return Message().conversation(id)

@messages.route('/message_all/')
def m_all():
    return Message().all_messages()