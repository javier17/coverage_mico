
from datetime import date, datetime, timedelta
from micro_project.src import create_app
import logging
import pytest
from flask_restful import Api
import hashlib
import bcrypt
from flask_jwt_extended import JWTManager
from faker import Faker
from flask_jwt_extended import create_access_token
from micro_project.src.models.models import Project , Company ,Functionary,  db

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

    yield _app
    ctx.pop()
    return _app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client



@pytest.fixture
def base_data(app):
    data =[]

    functionary = Functionary(person_id = 1, company_id = 1, rol = 'Analista')
    db.session.add(functionary)
    db.session.commit()

    company = Company(name='Compañia', address='Carrera 16', phone = '5454545', location = 'Colombia', sector_id = 1, type_id = 1)
    db.session.add(company)
    db.session.commit()

    project = Project (company_id = 1, name = 'Proyecto 1', description = 'Ejemplo Test', status = 'Activo')  
    db.session.add(project)
    db.session.commit()

    yield data
    



