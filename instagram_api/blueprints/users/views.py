from flask import Blueprint, jsonify
from models.user import User
from app import csrf


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
@csrf.exempt
def index():
    
    # user = User.select()
    
    users = [   
        {
            "id" : user.id,
            "username": user.username,
            "profileImage": user.profile_image_url
        } for user in User.select()
    ]
    
    response = jsonify(users)
    response.status_code = 200
    
    return response
    
 
