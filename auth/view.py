from flask import Blueprint 
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

@auth.route('/user_admin/')
def u_admin():
    return User().all_user_admin()