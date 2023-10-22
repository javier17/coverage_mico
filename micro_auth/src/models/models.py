from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

REFRESH_TOKENS = 'tokens'

class RefreshToken(db.Model):
    __tablename__ = REFRESH_TOKENS
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(2000), unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

class RefreshTokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RefreshToken
        include_relationships = True
        load_instance = True
