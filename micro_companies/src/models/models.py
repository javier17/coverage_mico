

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

COMPANIES_DB_NAME = 'companies'
COMPANY_TYPE_DB_NAME = 'company_types'
COMPANY_SECTOR_DB_NAME = 'company_sectors'


class Company(db.Model):
    __tablename__ = COMPANIES_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) , nullable=False)
    address = db.Column(db.String(200) , nullable=False)

    phone = db.Column(db.String(30) , nullable=False)
    location = db.Column(db.String(200) , nullable=False)

    sector_id = db.Column(db.Integer, db.ForeignKey('company_sectors.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('company_types.id'), nullable=False)
    rol = db.Column(db.String(100) , nullable=False)

    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)

    salt = db.Column(db.String(400))
    token = db.Column(db.String(400))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)


class CompanySector(db.Model):
    __tablename__ = COMPANY_SECTOR_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    company_types = db.relationship(
        'CompanyType', backref='company_sectors', lazy=True
    )


class CompanyType(db.Model):
    __tablename__ = COMPANY_TYPE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    sector_id = db.Column(db.Integer, db.ForeignKey(f'{COMPANY_SECTOR_DB_NAME}.id'), nullable=False)


class CompanyShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True


class CompanyTypesShema(SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyType
        include_relationships = True
        load_instance = True


class CompanySectorsShema(SQLAlchemyAutoSchema):
    class Meta:
        model = CompanySector
        include_relationships = True
        load_instance = True