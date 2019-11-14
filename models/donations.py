import peewee as pw

from models.base_model import BaseModel
from models.user import User
from models.images import Image

class Donation(BaseModel):
    username = pw.ForeignKeyField(User)
    image = pw.ForeignKeyField(Image)
    amount = pw.DecimalField()