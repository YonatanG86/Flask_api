from flask import jsonify
from flask.globals import session
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*arg,**kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return jsonify({"error": "No user is logged in"}), 400
    return wrap