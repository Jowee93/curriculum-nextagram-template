from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(null=True, unique=True)
    password = pw.CharField(null=False)
    
    def validate(self):
        duplicate_useremail = User.get_or_none(User.email == self.email)
        
        if duplicate_useremail:
            self.errors.append('Email has been taken. Please try another email')
