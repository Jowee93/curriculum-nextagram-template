import peewee as pw

from config import Config
from models.base_model import BaseModel
from models.user import User

class Follower(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)

