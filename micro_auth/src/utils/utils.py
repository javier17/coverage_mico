import hashlib
import json
import os
import random
from datetime import datetime, timedelta
from enum import Enum
from http import HTTPStatus

import bcrypt
import jwt
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.orm import (ColumnProperty, InstrumentedAttribute,
                            RelationshipProperty)
from sqlalchemy.orm.attributes import InstrumentedAttribute

from micro_auth.src.models.models import RefreshToken, db


class DbService:

    def __init__(self):
        pass

    def db_generic_create(data, model_class):
        new_instance = model_class()
        DbTools.assign_related_fields(data, model_class, new_instance)
        db.session.add(new_instance)
        db.session.commit()

        return ResponseTools.build_response(message=f'{model_class.__name__} created successfully', code=201, response=DbTools.model_instance_to_dict(new_instance))

    def clean_expired_tokens(self):
        date_now = datetime.now()
        RefreshToken.query.filter(
            RefreshToken.expiration_date <= date_now).delete()
        db.session.commit()


class DbTools:

    def model_instance_to_dict(instance, mapped_instances=None):
        if mapped_instances is None:
            mapped_instances = set()

        if instance in mapped_instances:
            return None

        mapped_instances.add(instance)

        result = {}

        # Mapear las columnas directas
        for attr in instance.__class__.__table__.columns.keys():
            result[attr] = getattr(instance, attr)

        # Mapear las relaciones
        for attr, prop in instance.__mapper__.relationships.items():
            if prop.uselist:
                result[attr] = [DbTools.model_instance_to_dict(
                    obj, mapped_instances) for obj in getattr(instance, attr)]
            else:
                result[attr] = DbTools.model_instance_to_dict(
                    getattr(instance, attr), mapped_instances)

        return result

    def assign_related_fields(data, model_class, model_instance):
        for field, value in data.items():
            if not hasattr(model_class, field) or getattr(getattr(model_class, field), 'primary_key', False):
                continue

            new_value = value
            attr = getattr(model_class, field)
            if isinstance(attr.property, RelationshipProperty):
                related_instances = attr.property.mapper.class_.query.filter(
                    attr.property.mapper.class_.id.in_(value)).all()

                if len(related_instances) != len(value):
                    valid_ids = [instance.id for instance in related_instances]
                    invalid_ids = [id for id in value if id not in valid_ids]
                    message = f'The following related IDs are invalid in {field} field : ' + ','.join(
                        map(str, invalid_ids))
                    raise ValueError(ResponseTools.build_response(
                        message=message, code=400))

                new_value = related_instances

            setattr(model_instance, field, new_value)


class ResponseTools:
    def map_response_code_to_type(response_code):
        response_ranges = {
            range(100, 400): ResponseType.SUCCESS,
            range(400, 600): ResponseType.ERROR,
        }

        for code_range, response_type in response_ranges.items():
            if response_code in code_range:
                return response_type

        return None

    def build_response(code=200, message=None, response=None, error_message=None):
        response_type = ResponseTools.map_response_code_to_type(code)

        if response_type is None:
            raise ValueError("Invalid response code")

        result = {
            "status": {
                "type": response_type.value,
                "code": code,
                "message": message or HTTPStatus(code).description,
                "errorMessage": error_message
            },
            "response": response
        }

        return result


class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


class SecurityTools:

    def get_tokendata(request):
        token = request.headers.environ['HTTP_AUTHORIZATION'].split("Bearer ")[
            1]
        data = jwt.decode(
            token,  current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
        return data

    def generate_token(data):
        expires_delta = timedelta(minutes=random.randint(5, 10))
        token = create_access_token(identity=json.dumps(
            data), expires_delta=expires_delta)

        return token

    def generate_refresh_token(data):

        expires_delta = timedelta(minutes=random.randint(5, 10))
        token = create_refresh_token(
            identity=data, expires_delta=expires_delta)

        return token, expires_delta

    def hash_password(password):
        sal = bcrypt.gensalt().decode()
        salted_password = password + sal
        passw = hashlib.sha256(salted_password.encode()).hexdigest()
        return {'password': passw, 'salt': sal}

    def verify_password(input_password, stored_password_hash, salt):
        salted_password = input_password + salt
        input_password_hash = hashlib.sha256(
            salted_password.encode()).hexdigest()
        return input_password_hash == stored_password_hash


""" 
json_data = {
    "_filters": [
        {"field": "username", "operator": "eq",
            "value": "john_doe", "logic": "AND"},
        {"field": "email", "operator": "contains",
            "value": "example.com", "logic": "OR"}
    ],
    "_joins": [
        {"type": "inner", "table": "rol", "onclause": "user.rol_id = rol.id"}
    ],
    "_order_by": [
        {"field": "createdAt", "direction": "desc"},
        {"field": "username", "direction": "asc"}
    ],
    "_page": 1,
    "_per_page": 10,
    "_select_fields": ["id", "username", "email"]
}
 """
