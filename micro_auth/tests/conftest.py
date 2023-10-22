
from datetime import date, datetime, timedelta
from micro_auth.src import create_app
import logging
import pytest
from flask_restful import Api
import hashlib
import bcrypt
from flask_jwt_extended import JWTManager
from faker import Faker
from flask_jwt_extended import create_access_token
from micro_auth.src.models.models import db, RefreshToken

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
    token1 = RefreshToken(token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg', expiration_date = datetime(2028, 12, 31, 11, 59, 59))

    data.append(
        {"token": token1.token}
    )

    db.session.add(token1)
    db.session.commit()

    refresh_token = RefreshToken.query.filter_by(token=token1.token).first()

    print('bd')
    print(refresh_token.token)
    print('bd')

    yield data
    
