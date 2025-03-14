from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.followers.views import followers_blueprint
from instagram_web.blueprints.inboxes.views import inboxes_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.util.google_oauth import oauth
from models.user import *
from models.inboxes import *


assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followers_blueprint, url_prefix="/followers")
app.register_blueprint(inboxes_blueprint, url_prefix="/inboxes")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    users = User.select().order_by(User.id)
       
    return render_template('home.html', users=users)



