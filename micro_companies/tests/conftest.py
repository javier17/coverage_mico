
from datetime import date, datetime, timedelta
from micro_companies.src import create_app
import logging
import pytest
from micro_companies.src.models.models import db, CompanySector, CompanyType, Company
from flask_restful import Api
import hashlib
import bcrypt
from flask_jwt_extended import JWTManager
from faker import Faker
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app('default')
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    _app.config["TESTING"] = True
    _app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
    _app.testing = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    print(_app.config["SQLALCHEMY_DATABASE_URI"])
    with _app.app_context():
        db.init_app(_app)
        db.create_all()

    api = Api(_app)
   
    jwt = JWTManager(_app)

    yield _app
    ctx.pop()
    return _app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def base_data(app):
    sector1 = CompanySector(name = 'Tecnología')
    db.session.add(sector1)
    db.session.commit()

    sector1 = db.session.get(CompanySector, 1)
    tipo1 = CompanyType(name = 'Empresas de software',  sector_id=sector1.id)
    
    db.session.add(tipo1)
    db.session.commit()

    data = []
    fake = Faker()
    for x in range(10):
        name = fake.user_name()
        address = fake.street_address()

        email = fake.email()
        phone = fake.phone_number()
        rol = fake.job()
        location = fake.country()

 
        password = fake.password(length=12)

        expires_delta = timedelta(minutes=25)
        token = create_access_token(identity={
                                        'id':x ,'username': name, 'email': email}, expires_delta=expires_delta)
        data.append(
            {"id": x,"name": name, "email": email, "password": password,"token":token})

        salt = bcrypt.gensalt().decode()
        salted_password = password + salt
        hashlib_password = hashlib.sha256(
            salted_password.encode()).hexdigest()
            
        company = Company(name=name, address=address, email=email, phone = phone, location = location, rol = rol, sector_id= sector1.id, type_id = tipo1.id ,password=hashlib_password,
                    salt=salt, token=token, expireAt=datetime.now(), createdAt=datetime.now()+expires_delta)
        db.session.add(company)
        db.session.commit()

    yield data
    
