from flask import Blueprint, render_template, redirect, request, url_for, flash
from models.followers import *
from models.inboxes import *
from flask_login import login_required, current_user

followers_blueprint = Blueprint('followers', 
                                __name__, 
                                template_folder='templates')



@followers_blueprint.route('/follow', methods=['POST'])
def follow():
    user_id = request.form.get('user_id')
    inbox = Inbox(user=user_id, requestor=current_user.id, status="Pending")
    inbox.save()
    
    follow = Follower(user=user_id, follower=current_user.id, status=False)
    follow.save()    
    
    return redirect(url_for('images.show', id=user_id, inbox=inbox))

@followers_blueprint.route('/unfollow', methods=['POST'])
def unfollow():
    user_id = request.form.get('user_id')
    
    following = Follower.following
    all_following = []
    
    for i in following:
        all_following.append(i)
        
    user_unfollow = Follower.get(user_id=user_id, follower_id=current_user.id)    
    user_unfollow.delete_instance()
    
    return redirect(url_for('images.show', id=user_id))
