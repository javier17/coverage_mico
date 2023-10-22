from flask import Blueprint, request

from micro_companies.src.models.models import Company, CompanyShema
from micro_companies.src.services.security import *
from micro_companies.src.utils.decorators import *
from micro_companies.src.utils.utils import *

mod = Blueprint('auth_controller', __name__)
company_schema  = CompanyShema()
base_url = '/auth'
company_entity = Company

@mod.route(f'{base_url}/login', methods=['POST'])
@handle_error
@validate_required_fields(['email', 'password'])
def login():

    u_email = request.json['email']
    u_password = request.json['password']

    company = company_entity.query.filter_by(email=u_email).first()

    if not company or not DbTools.verify_password(u_password, company.password, company.salt):
        return ResponseTools.build_response(message="El correo o contraseña son incorrectos", code=404)

    if not company.active:
        return ResponseTools.build_response(message="El usuario no esta activo", code=404)

    user_dict = company_schema.dump(company)

    tokens = SecurityService.generate_token(user_dict)
 

    response = {
        'id': company.id,
        'token': tokens["token"],
        'name': user_dict["name"],
        'email': user_dict["email"],
        'refresh_token': tokens["refresh_token"],
        "expiration_date": tokens["expiration_date"],
        'message': 'Successfully generated token',
        "error": False
    }

    return ResponseTools.build_response(response=response)

@mod.route(f'{base_url}/me', methods=['GET'])
@authorizer()
@handle_error
def get_me():
    return SecurityService.get_tokendata(request)
    