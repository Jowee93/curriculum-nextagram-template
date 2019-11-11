from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import *
from werkzeug.security import generate_password_hash
import re


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form.get("password")
    user_name = request.form.get("username")
    user_email = request.form.get("email")
    
    if len(user_password) < 6 :
        flash("Password must be more than 6 characters !", "danger")
        return render_template('users/new.html')
    elif not re.search(r"([A-Z]+[a-z]+|[a-z]+[A-Z]+)", user_password):
        flash("Password must contain at least one(1) upper and one(1) lower case", "danger")
        return render_template('users/new.html')
    elif not re.search(r"[!@#0^&*()+]+", user_password):
        flash("Password must contain at least one(1) special character", "danger")
        return render_template('users/new.html')
    
    user_hashed_password = generate_password_hash(user_password)
    
    new_user = User(username=user_name, email=user_email, password=user_hashed_password)
    

    if new_user.save():
        flash("Successfully signed up !", "success")
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', error=new_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass



