from flask import Blueprint

conversations = Blueprint('conversations', __name__)

@conversations.route('/')
def about():
    return 'Those are real conversations I had with my family'