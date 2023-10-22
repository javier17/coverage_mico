from functools import wraps

from flask import request

from jwt.exceptions import ExpiredSignatureError
from micro_companies.src.models.models import db
from micro_companies.src.utils.utils import *
from micro_companies.src.services.security import *

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

