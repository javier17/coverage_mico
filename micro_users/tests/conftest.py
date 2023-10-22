import os
from datetime import date, datetime, timedelta
from micro_users.src import create_app
import logging
import pytest
from flask_restful import Api
from flask_cors import CORS
import hashlib
import bcrypt
from flask_jwt_extended import JWTManager
from faker import Faker
from flask_jwt_extended import create_access_token
from micro_users.src.models.models import db, User

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
    data = []
    fake = Faker()
    for x in range(10):
        fk_email = fake.email()
        fullname = fake.name()
        phone = fake.phone_number()
        country = fake.country()
        email=fk_email
        password = fake.password(length=12)
        expires_delta = timedelta(minutes=25)
        token = create_access_token(identity={
                                        'id':x ,'email': email}, expires_delta=expires_delta)
        data.append(
            {"email": email, "password": password, "token":token})

        salt = bcrypt.gensalt().decode()
        salted_password = password + salt
        hashlib_password = hashlib.sha256(
            salted_password.encode()).hexdigest()

            
        user = User(fullname=fullname, phone=phone, country=country, email=email, password=hashlib_password,
                    salt=salt, token=token, expireAt=datetime.now(), createdAt=datetime.now()+expires_delta)
        db.session.add(user)
        db.session.commit()

    yield data
