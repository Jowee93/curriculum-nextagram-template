from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(null=True, unique=True)
    password = pw.CharField(null=True)
    
    def validate(self):
        duplicate_useremail = User.get_or_none(User.email == self.email)
        
        if duplicate_useremail:
            self.errors.append('Email has been taken. Please try another email')
            
    # def is_authenticated(self):
    #     return True
            

