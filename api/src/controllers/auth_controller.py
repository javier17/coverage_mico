from flask import Blueprint, request
from api.src.services.auth_service import AuthService
from api.src.utils.decorators import handle_error, authorizer
from flask_cors import cross_origin

mod = Blueprint('auth_controller', __name__)
base_url = '/api/auth'
service = AuthService

@cross_origin
@mod.route(f'{base_url}/refresh', methods=['GET'])
@handle_error
@authorizer()
def refresh():

    return service.refresh(request.headers)
