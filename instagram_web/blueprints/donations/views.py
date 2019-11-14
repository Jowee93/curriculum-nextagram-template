from flask import Blueprint, render_template, request, redirect, url_for, flash

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')

