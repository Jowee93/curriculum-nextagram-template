import peewee as pw
from playhouse.hybrid import hybrid_property

from config import Config
from flask_login import UserMixin
from models.base_model import BaseModel
from models.user import User


class Image(UserMixin, BaseModel):
    image = pw.TextField(null=True)
    username = pw.ForeignKeyField(User)
    
    
    def is_authenticated(self):
        return True
    
    
    @hybrid_property
    def image_url(self):
        return Config.S3_LOCATION + self.image
