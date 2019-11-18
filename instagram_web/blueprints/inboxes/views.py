from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.inboxes import Inbox
from models.followers import Follower

inboxes_blueprint = Blueprint('inboxes', 
                                __name__, 
                                template_folder='templates')


@inboxes_blueprint.route('/<id>/inbox', methods=['GET'])
def show(id):
    
    user = User.get_by_id(id)
    
    # user_inbox = Inbox.select().join(User, on=Inbox.user).where(Inbox.user_id==current_user.id)
    user_inbox = User.select().join(Inbox, on=Inbox.requestor_id).where(Inbox.user_id==user.id)
    
    
    return render_template('inboxes/new.html', user_inbox=user_inbox)

@inboxes_blueprint.route('/<id>/destroy', methods=['POST'])
def destroy(id):
    
    user = User.get_by_id(id)
    user_id = request.form.get('user_id')
    
    follow = Follower.update(status=True).where(Follower.user_id==current_user.id, Follower.follower_id==user_id)
    
    follow.execute()
    
    # delete = Inbox.get(Inbox.user_id==current_user.id)
    delete = Inbox.delete().where(Inbox.user_id==current_user.id and Inbox.requestor_id==user_id)
    delete.execute()
    
    return redirect(url_for('inboxes.show', id=current_user.id))
    


