from flask import Blueprint, request
from api.src.services.company_service import CompanyService
from api.src.utils.decorators import handle_error, authorizer

mod = Blueprint('company_controller', __name__)
base_url = '/api/companies'
service = CompanyService


@mod.route(f'{base_url}', methods=['POST'])
@handle_error
def create():
    return service.create(request.json)


@mod.route(f'{base_url}/login', methods=['POST'])
@handle_error
def login():
    return service.login(request.json)


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
@authorizer()
def get_by_id(model_id):

    return service.get_by_id(model_id)


@mod.route(f'{base_url}/me', methods=['GET'])
@handle_error
@authorizer()
def get_me():

    return service.get_me()