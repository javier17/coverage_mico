from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

USER_DB_NAME = 'user'
CASCADE_FULL_DB = 'all, delete, delete-orphan'

class AccessEnum(str, Enum):
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    CREATE = 'create'


class User(db.Model):
    __tablename__ = USER_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(64), unique=True)
    country = db.Column(db.String(50))
    password = db.Column(db.String(400))
    salt = db.Column(db.String(400))
    token = db.Column(db.String(400))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)    


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True