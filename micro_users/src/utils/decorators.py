from functools import wraps

from flask import request
import jwt
from jwt.exceptions import ExpiredSignatureError
from micro_users.src.models.models import User, db
from micro_users.src.services.security import *
from micro_users.src.utils.utils import *


def authorizer():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):            
            data = SecurityService.get_tokendata(request)     
            if not data:
                return ResponseTools.build_response(message='Unauthorized', code=401)
           
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ss_password_auth():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):            
            data = SecurityService.get_tokendata(request) 
            kwargs['data'] = data      
            if not data:
                return ResponseTools.build_response(message='Unauthorized', code=401)
           
            return func(*args, **kwargs)
        return wrapper
    return decorator


def handle_error(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ExpiredSignatureError as e:
            db.session.rollback()
            message = 'Failed authentication'
            error_message = str(e)
            return ResponseTools.build_response(message=message, error_message=error_message, code=401)
        except Exception as e:
            db.session.rollback()
            message = 'Unexpected error'
            error_message = str(e)
            return ResponseTools.build_response(message=message, error_message=error_message, code=500)
    return decorated


def validate_required_fields(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_data = request.json
            missing_fields = [
                field for field in required_fields if field not in request_data]

            if missing_fields:
                message = f'Missing required fields: {", ".join(missing_fields)}'
                return ResponseTools.build_response(message=message, code=400)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def authenticate_and_authorize(rols=None):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                token_data = SecurityService.get_tokendata(request)
                user_id = token_data.get('id')
                user = User.query.get(user_id)
                if rols and user.rol not in rols:
                    return {'message': 'Acceso no autorizado', 'error': True}, 403
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {'message': 'Token expirado', 'error': True}, 401
            except jwt.InvalidTokenError:
                return {'message': 'Token inválido', 'error': True}, 401
        return decorated
    return decorator
