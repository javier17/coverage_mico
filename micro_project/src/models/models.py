

from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


PERSON_TABLE_DB_NAME = 'person'
FUNCTIONARY_TABLE_DB_NAME = 'functionary'
COMPANY_TABLE_DB_NAME = 'company'
COMPANY_TYPE_DB_NAME = 'company_types'
COMPANY_SECTOR_DB_NAME = 'company_sectors'
CANDIDATE_DB_NAME = 'candidate'
PROJECT_DB_NAME = 'project'
PROFILE_DB_NAME = 'profile'


class Person(db.Model):
    __tablename__ = PERSON_TABLE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    geographic_location = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    salt = db.Column(db.String(400))
    token = db.Column(db.String(400))
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    candidate = db.relationship("Candidate", cascade="all,delete", backref="person")
    functionary = db.relationship("Functionary", cascade="all,delete", backref="person")


class Candidate(db.Model):
    __tablename__ = CANDIDATE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    dob = db.Column(db.Date)
    languages = db.Column(db.String(255))


class Functionary(db.Model):
    __tablename__ = FUNCTIONARY_TABLE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    rol = db.Column(db.String(50))


class Company(db.Model):
    __tablename__ = COMPANY_TABLE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30) , nullable=False)
    address = db.Column(db.String(200) , nullable=False)
    phone = db.Column(db.String(30) , nullable=False)
    location = db.Column(db.String(200) , nullable=False)

    sector_id = db.Column(db.Integer, db.ForeignKey('company_sectors.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('company_types.id'), nullable=False)



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


class Project(db.Model):
    __tablename__ =  PROJECT_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id') , nullable=False)
    name = db.Column(db.String(50), unique=True , nullable=False)
    description = db.Column(db.String(200) , nullable=False)
    status = db.Column(db.String(50) , nullable=False)
    profile = db.relationship('Profile', back_populates='project', uselist=False,  cascade="all,delete")


class Profile(db.Model):
    __tablename__ =  PROFILE_DB_NAME
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100) , nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id') , nullable=False)
    project = db.relationship('Project', back_populates='profile')


class PersonShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True


class CandidateShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Candidate
        include_relationships = True
        load_instance = True

class CompanyShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_relationships = True
        load_instance = True

class FunctionaryShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Functionary
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


class ProjectShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True


class ProfileShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_relationships = True
        load_instance = True
