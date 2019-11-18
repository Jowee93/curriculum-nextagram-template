from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user

inboxes_blueprint = Blueprint('inboxes', 
                                __name__, 
                                template_folder='templates')


@inboxes_blueprint.route('/<id>/inbox', methods=['GET'])
def show(id):
    pass


