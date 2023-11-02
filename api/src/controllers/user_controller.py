from flask import Blueprint, request
from api.src.services.user_service import UserService
from api.src.utils.decorators import *
from api.src.utils.utils import *

from flask_cors import cross_origin

mod = Blueprint('users_controller', __name__)
base_url = '/api/users'
service = UserService

@cross_origin
@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
@authorizer('read', 'users')
def get_by_id(model_id):
    return service.get_by_id(model_id)

@cross_origin
@mod.route(f'{base_url}/me', methods=['GET'])
@handle_error
@authorizer()
def get_by_token():
    return service.get_by_token()

@cross_origin
@mod.route(f'{base_url}/all', methods=['POST'])
@handle_error
@authorizer('read', 'users')
def get_all():
    return service.get_all(request.json)

@cross_origin
@mod.route(f'{base_url}', methods=['POST'])
@handle_error
def create():
    return service.create(request.json)

@cross_origin
@mod.route(f'{base_url}/password', methods=['POST'])
@handle_error
@authorizer()
def password():
    return service.password(request.json)

@cross_origin
@mod.route(f'{base_url}/<int:model_id>', methods=['PUT'])
@handle_error
@authorizer('update', 'users')
def update(model_id):
    return service.update(model_id, request.json)

@cross_origin
@mod.route(f'{base_url}/<int:model_id>', methods=['DELETE'])
@handle_error
@authorizer('delete', 'users')
def delete(model_id):
    return service.delete(model_id)

@cross_origin
@mod.route(f'{base_url}/login', methods=['POST'])
@handle_error
def login():
    return service.login(request.json)
