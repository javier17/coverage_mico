from flask import Blueprint, request

from micro_users.src.models.models import UserSchema
from micro_users.src.services.security import *
from micro_users.src.utils.decorators import *
from micro_users.src.utils.utils import *

mod = Blueprint('auth_controller', __name__)
user_schema = UserSchema()
base_url = '/auth'
user_entity = User


@mod.route(f'{base_url}/login', methods=['POST'])
@handle_error
@validate_required_fields(['email', 'password'])
def login():

    u_email = request.json['email']
    u_password = request.json['password']

    user = user_entity.query.filter_by(email=u_email).first()

    if not user or not DbTools.verify_password(u_password, user.password, user.salt):
        return ResponseTools.build_response(message="El email o contraseña son incorrectos", code=404)

    if not user.active:
        return ResponseTools.build_response(message="El usuario no esta activo", code=404)

    user_dict = user_schema.dump(user)
    
    tokens = SecurityService.generate_token(user_dict)

    response = {
        'id': user.id,
        'token': tokens["token"],
        'email': user_dict["email"],
        'fullname': user_dict["fullname"],
        'refresh_token': tokens["refresh_token"],
        "country": user_dict["country"],
        "expiration_date": tokens["expiration_date"],
        'message': 'Successfully generated token',
        "error": False
    }

    return ResponseTools.build_response(response=response)
