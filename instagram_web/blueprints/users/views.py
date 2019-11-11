from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import *
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form.get("password")
    user_hashed_password = generate_password_hash(user_password)
    
    new_user = User(username=request.form.get("username"), email=request.form.get("email"), password=user_hashed_password)
    
    
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



