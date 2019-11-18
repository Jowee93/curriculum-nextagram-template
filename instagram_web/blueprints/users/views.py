from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
from flask_login import login_required, current_user
from instagram_web.util.helpers import *    
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
@login_required
def edit(id):
    user = User.get_by_id(id)
    
    if current_user.id == user.id:
        return render_template('/users/edit.html', user_id=user.id)
    else:
        flash("You are not authorized to access this page", "danger")
        return render_template('/users/edit.html', user_id=user.id)
    
    
@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    description = request.form.get("description")
    
    result = check_password_hash(user.password, password)
    
    if result:
        if user.email == email:
            update_user = User(id=user.id, username=username, description=description)
            if update_user.save(only=[User.username, User.description]):
                flash(f"Successfully updated profile for: {current_user.username}", "success")
                return redirect(url_for('users.edit', id=current_user.id))
            else:
                flash(f"Error: {update_user.errors}", "danger")
                return redirect(url_for('users.edit', id=current_user.id))
        else:
            update_user = User(id=user.id, username=username, email=email, description=description)
            if update_user.save():
                flash(f"Successfully updated profile for: {current_user.username}", "success")
                return redirect(url_for('users.edit', id=current_user.id))
            else:
                flash(f"Error: {update_user.errors}", "danger")
                return redirect(url_for('users.edit', id=current_user.id))
    else:
        flash("Password incorrect, please try again", "danger")
        return render_template('/users/edit.html', user_id=user.id)
    
    
@users_blueprint.route('/<id>/uploadimage', methods=['GET'])
@login_required
def image(id):
    
    user = User.get_by_id(id)
    return render_template('users/upload.html', id=current_user.id)

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    
    # Retrieves file from upload form
    file = request.files.get("user_file")
    
    user = User.get_by_id(id)
    
    if not file:
        flash("Please choose a file to upload", "danger")
        return render_template('users/upload.html')
    
    # Makes file name secure (without spacing etc.)
    file.filename = secure_filename(file.filename)
    output = upload_file_to_s3(file)
    
    if not output:
        flash("Upload was unsuccessful, please try again", "danger")
        return render_template('users/upload.html')
    
    else:
        flash("Profile image updated successful!", "success")
        upload_image = User.update(image=output).where(User.id == user.id)
        upload_image.execute()
        return redirect(url_for('users.image', id=current_user.id))
    
    
    
    
    
    
    
    
    
    


