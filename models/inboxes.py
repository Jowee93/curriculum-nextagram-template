import peewee as pw

from config import Config
from models.base_model import BaseModel
from models.user import User
from models.followers import Follower
from flask_login import current_user
from playhouse.hybrid import hybrid_property

class Inbox(BaseModel):
    user_request = pw.ForeignKeyField(Follower)
    status = pw.CharField(default="Pending")