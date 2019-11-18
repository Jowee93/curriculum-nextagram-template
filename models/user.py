import peewee as pw
from playhouse.hybrid import hybrid_property

from config import Config
from flask_login import UserMixin
from models.base_model import BaseModel


class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(null=True, unique=True)
    password = pw.CharField(null=True)
    role = pw.CharField(default="user")
    image = pw.TextField(null=True)
    
    def validate(self):
        duplicate_useremail = User.get_or_none(User.email == self.email)
        
        if duplicate_useremail:
            self.errors.append('Email has been taken. Please try another email')
            
    def is_authenticated(self):
        return True
    
    @hybrid_property
    def profile_image_url(self):
        return Config.S3_LOCATION + self.image
