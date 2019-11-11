from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import *
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')




@sessions_blueprint.route('/signin', methods=['GET'])
def sign_in():
    return render_template('sessions/sign_in.html')


@sessions_blueprint.route('/signin', methods=['POST'])
def handle_sign_in():
    
    username = request.forms.get("username")
    password = request.forms.get("password")
    
    
    return render_template('sessions/sign_in.html')