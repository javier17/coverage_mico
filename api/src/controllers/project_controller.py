from flask import Blueprint, request
from api.src.services.project_service import ProjectService
from api.src.utils.decorators import handle_error, authorizer
from api.src.utils.utils import *


mod = Blueprint('project_controller', __name__)
base_url = '/api/projects'
service = ProjectService

@mod.route(f'{base_url}', methods=['POST'])
@handle_error
@authorizer()
def create():
    return service.create(request.json)


@mod.route(f'{base_url}/<int:model_id>', methods=['PUT'])
@handle_error
@authorizer()
def update(model_id):
    return service.update(model_id, request.json)


@mod.route(f'{base_url}/<int:model_id>', methods=['DELETE'])
@handle_error
@authorizer()
def delete(model_id):
    return service.delete(model_id)


@mod.route(f'{base_url}', methods=['GET'])
@handle_error
@authorizer()
def get_all():
    return service.get_all()

