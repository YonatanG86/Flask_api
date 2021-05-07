from flask import Blueprint 
from functools import wraps
from model.user_model import User
from utilities.utilities import login_required

auth = Blueprint('auth', __name__)

@auth.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@auth.route('/user/login', methods=['POST'])
def login():
    return User().login()


@auth.route('/user/logout')
@login_required
def logout():
    return User().logout()