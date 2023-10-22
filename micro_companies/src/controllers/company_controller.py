import hashlib
import re
from datetime import datetime, timedelta

import jwt
import bcrypt

from flask import Blueprint, request

from micro_companies.src.models.models import Company, CompanyShema, db
from micro_companies.src.utils.decorators import *
from micro_companies.src.utils.utils import *


mod = Blueprint('company_controller',__name__)
model_schema = CompanyShema()
base_url = '/companies'
entity = Company

@mod.route(f'{base_url}', methods=['POST'])
@handle_error
@validate_required_fields(['name', 'address', 'phone', 'email', 'password', 'location'])
def create():
    c_name = request.json['name']
    c_address = request.json['address']

    c_phone = request.json['phone']
    c_location = request.json['location']

    c_sector_id = request.json['sector_id']
    c_type_id = request.json['type_id']
    c_rol= request.json['rol']


    c_email = request.json['email']
    c_password = request.json['password']

 
    
    if not (CompanyTools.check_email(c_email)):
        message = 'Invalid email'
        return ResponseTools.build_response(code=412, message=message)

    company = entity.query.filter((entity.name.ilike(c_name)) | (
        entity.email.ilike(c_email))).first()
    
    if company:
        message = 'The company entered already exists'
        return ResponseTools.build_response(code=412, message=message)
    
    hashlib_password = DbTools.hash_password(c_password)
    today = datetime.now()

    data = {
        'name': c_name,
        'address': c_address,

        'phone': c_phone,
        'location': c_location,

        'sector_id': c_sector_id,
        'type_id': c_type_id,
        'rol':  c_rol,

        'email': c_email,
        'password': hashlib_password['password'],
        'salt': hashlib_password['salt'],
        'token': '',
        'expireAt': today + timedelta(minutes=25),
        'createdAt': today
    }

    response = DbService.db_generic_create(data, entity)
    keys_to_remove = ['createdAt', 'expireAt', 'password', 'salt']
    response['response'] = {key: value for key, value in response['response'].items(
    ) if key not in keys_to_remove}
    return response


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
@authorizer()
def get_by_id(model_id):

    json_data = {"_select_fields": [
        "id", "name", 'address', 'phone', 'rol', 'sector_id', 'location']
    }
    response = DbService.db_generic_get_by_id(
        model_class=entity, model_id=model_id, json_data=json_data)
    return response


class CompanyTools:
    def check_name(name):
        regex = r'^[a-zA-Z0-9_.-]{3,32}$'
        if (re.match(regex, name)):
            return True
        else:
            return False

    def check_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False
