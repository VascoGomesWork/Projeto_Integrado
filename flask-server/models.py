from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def get_uuid():
    return uuid4().hex

# TABLES
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text(), nullable=False)

class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class Tools(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(345))
    quantity = db.Column(db.Integer)

class ToolsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tools
