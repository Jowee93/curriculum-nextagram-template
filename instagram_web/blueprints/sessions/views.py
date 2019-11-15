from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import *
from werkzeug.security import check_password_hash
import time
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from instagram_web.util.google_oauth import oauth



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')



@sessions_blueprint.route('/signin', methods=['GET'])
def sign_in():
    
    return render_template('sessions/sign_in.html')


@sessions_blueprint.route('/signin', methods=['POST'])
def handle_sign_in():
    username = request.form.get("username")
    password = request.form.get("password")
    
    user = User.get_or_none(username=username)

    if user:
        result = check_password_hash(user.password, password)
        
        if result:
            flash("You are logged in", "success")
            login_user(user)
            # session["user_id"] = user.id
            return redirect("/")
        
        else:
            flash("Log in fail, please try again", "danger")
            return render_template('sessions/sign_in.html')
    
    else:
        flash("Username or Password is incorrect. Please try again", "danger")
        return render_template('sessions/sign_in.html')
    
@sessions_blueprint.route('/login/google', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize_google():
    token = oauth.google.authorize_access_token()
    
    if not token:
        flash("Something went wrong, please try again", "danger")
        return redirect(url_for('sessions.signin'))

    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    
    user = User.get_or_none(User.email == email)
    
    if not user:
        flash("Sorry, no account registered with this email", "danger")
        return redirect(url_for('sessions.signin'))
    
    flash("Welcome back !", "success")
    login_user(user)
    return redirect('/')
        


@sessions_blueprint.route('/signout')
@login_required
def handle_sign_out():
    logout_user()
    # session.pop('user_id', None)
    flash("You have successfully logged out", "success")
    return redirect(url_for('sessions.sign_in'))
