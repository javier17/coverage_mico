
from datetime import date, datetime, timedelta
from src import create_app
import logging
import pytest
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
    _app.testing = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    print(_app.config["SQLALCHEMY_DATABASE_URI"])
   

    api = Api(_app)

    jwt = JWTManager(_app)

    yield _app
    ctx.pop()
    return _app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

