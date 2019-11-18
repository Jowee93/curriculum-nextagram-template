from flask import Blueprint, render_template, redirect, request, url_for, flash
from models.followers import *
from flask_login import login_required, current_user

followers_blueprint = Blueprint('followers', 
                                __name__, 
                                template_folder='templates')

