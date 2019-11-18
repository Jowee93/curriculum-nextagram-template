from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import *
from models.images import *
from models.followers import *
from flask_login import login_required, current_user
from werkzeug import secure_filename
from instagram_web.util.helpers import upload_file_to_s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/<id>/new', methods=['GET'])
@login_required
def new(id):
   return render_template('images/new.html', id=current_user.id)

@images_blueprint.route('/<id>/create', methods=['POST'])
@login_required
def create(id):
    
    image = request.files.get("user_image")
    user = User.get_by_id(id)
    
    if not image:
        flash("Please choose a file to upload", "danger")
        return render_template('images/new.html', id=current_user.id)
    
    image.filename = secure_filename(image.filename)
    output = upload_file_to_s3(image)
    
    if not output:
        flash("Upload was unsuccessful, please try again", "danger")
        return render_template('images/new.html', id=current_user.id)
    
    else:
        flash("Successfully posted !", "success")
        upload_image = Image(username_id=current_user.id, image=output)
        upload_image.save()
        return redirect(url_for('images.new', id=current_user.id))
    
@images_blueprint.route('/<id>/images', methods=['GET'])
@login_required
def show(id):
    
    user = User.get_by_id(id)
    
    following = Follower.following
    all_following = []
    
    for i in following:
        all_following.append(i)
      
    access = False
    
    
    query = Follower.select(Follower.status).where(Follower.user_id==user.id, Follower.follower_id==current_user.id)
    
    query_status = True
    
    for i in query:
        print("i is: ")
        print(i.status)
        query_status = i.status   
        
    
    if user in all_following:
        access = True
        
    user_following = User.select().join(Follower, on=Follower.user).where(Follower.follower==user.id)
    num_following = len(user_following)
    
    user_followers = User.select().join(Follower, on=Follower.follower).where(Follower.user==user.id)
    num_followers = len(user_followers)
    
    
    images = Image.select().join(User).where(Image.username==id)
    num_images = len(images)
    
    if query_status == False:
        flash("Awaiting follow request to be approved", "warning")
        return render_template('images/images.html', user_id=user.id, user=user, access=access, num_images=num_images, num_following=num_following, num_followers=num_followers, query_status=query_status)
    
    elif user.id == current_user.id or access == True:
        return render_template('images/images.html', images=images, user_id=user.id, user=user, access=access, num_images=num_images, num_following=num_following, num_followers=num_followers)
    
    else:
        flash("This page is private. Request to follow to be able to access this profile's page" , "danger")
        return render_template('images/images.html', user_id=user.id, user=user, access=access, num_images=num_images, num_following=num_following, num_followers=num_followers)
    
   
    
    
    
