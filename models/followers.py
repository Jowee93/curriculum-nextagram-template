import peewee as pw

from config import Config
from models.base_model import BaseModel
from models.user import User
from flask_login import current_user
from playhouse.hybrid import hybrid_property

class Follower(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    status = pw.BooleanField()

    @hybrid_property
    def following(self):
        return (User.select().join(Follower, on=Follower.user).where(Follower.follower==current_user.id))
    
    @hybrid_property
    def followers(self):
        return User.select().join(Follower, on=Follower.follower).where(Follower.user==current_user.id)
    
    def validate(self):
        pass
    