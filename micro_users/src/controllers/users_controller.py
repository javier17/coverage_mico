import hashlib
import re
from datetime import datetime, timedelta

import bcrypt
from flask import Blueprint, request
from micro_users.src.models.models import User, UserSchema, db
from micro_users.src.services.security import *
from micro_users.src.utils.decorators import *
from micro_users.src.utils.utils import *

mod = Blueprint('users_controller', __name__)
model_schema = UserSchema()
base_url = '/users'
entity = User


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
@authorizer()
def get_by_id(model_id):

    json_data = {"_select_fields": [
        "id", "email", 'fullname']}
    response = DbService.db_generic_get_by_id(
        model_class=entity, model_id=model_id, json_data=json_data)
    return response


@mod.route(f'{base_url}/filter', methods=['POST'])
@handle_error
@authorizer()
def get_all():
    default = ["password", "salt", 'token', "createdAt", "expireAt"]
    try:
        json_data = request.json
    except:
        json_data = {}

    response = DbService.db_generic_get(
        model_class=entity, json_data=json_data)
    # Eliminar campos de seguridad
    if response:
        for result in response['response']:
            for field in default:
                result.pop(field, None)

    return response


@mod.route(f'{base_url}/<int:model_id>', methods=['PUT'])
@handle_error
@authorizer()
@validate_required_fields(['email', 'username'])
def update(model_id):

    keys_to_remove = ['createdAt', 'expireAt', 'password', 'salt', 'token']

    for field in keys_to_remove:
        if field in request.json:
            del request.json[field]

    response = DbService.db_generic_update(model_id, request.json, entity)
    response['response'] = {key: value for key, value in response['response'].items(
    ) if key not in keys_to_remove}

    return response


@mod.route(f'{base_url}/<int:model_id>', methods=['DELETE'])
@handle_error
@authorizer()
def delete(model_id):

    return DbService.db_generic_delete(model_id, entity)


@mod.route(f'{base_url}', methods=['POST'])
@handle_error
@validate_required_fields(['fullname', 'phone','email', 'password', 'country'])
def create():
    u_fullname = request.json['fullname']
    u_phone = request.json['phone']
    u_country = request.json['country']
    u_password = request.json['password']
    u_email = request.json['email']

    if not (UserTools.check_email(u_email)):
        message = 'Invalid email'
        return ResponseTools.build_response(code=412, message=message)

    user = entity.query.filter((entity.email.ilike(u_email))).first()

    if user:
        message = 'The user entered already exists'
        return ResponseTools.build_response(code=412, message=message)

    hashlib_password = DbTools.hash_password(u_password)
    today = datetime.now()

    data = {
        'fullname' : u_fullname,
        'phone' : u_phone,
        'country' : u_country,
        'email': u_email,
        'password': hashlib_password['password'],
        'salt': hashlib_password['salt'],
        'token': '',
        'expireAt': today + timedelta(minutes=25),
        'createdAt': today,
        'id': 0
    }

    response = DbService.db_generic_create(data, entity)
    keys_to_remove = ['createdAt', 'expireAt', 'password', 'salt']
    response['response'] = {key: value for key, value in response['response'].items(
    ) if key not in keys_to_remove}
    return response


@mod.route(f'{base_url}/password', methods=['POST'])
@handle_error
@ss_password_auth()
@validate_required_fields(['password','new_password'])
def password(*args, **kwargs):
    u_password = request.json['password']
    new_password = request.json['new_password']
    data = kwargs.get('data')['id']

    user = entity.query.filter((entity.id == data)).first()

    if not user or not DbTools.verify_password(u_password, user.password, user.salt):
        return ResponseTools.build_response(message="El usuario o contraseña son incorrectos", code=404)

    if not user.id:
        message = 'The user doesnt exists'
        return ResponseTools.build_response(code=412, message=message)

    hashlib_password = DbTools.hash_password(new_password)
    today = datetime.now()
    user.password = hashlib_password['password']
    user.salt = hashlib_password['salt']

    db.session.commit()
    return ResponseTools.build_response(message=f'Password updated successfully')


class UserTools:
    def check_username(user):
        regex = r'^[a-zA-Z0-9_.-]{4,32}$'
        if (re.match(regex, user)):
            return True
        else:
            return False

    def check_password(user, password):
        salted_password = password + user.salt
        hashlib_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return hashlib_password == user.password

    def check_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False
