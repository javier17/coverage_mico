from functools import wraps

from flask import request
from api.src.services.auth_service import *
from api.src.utils.utils import *


def authorizer(access=None, level=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            data = AuthService.get_token_data(request)
            if not data:
                return ResponseTools.build_response(message='Unauthorized', code=401)

            permissions = data.get('permissions', [])
            if access and level:
                has_permission = any(permission.get('access') == access and permission.get(
                    'level') == level for permission in permissions)

                if not has_permission:
                    return ResponseTools.build_response(message='Unauthorized', code=401)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def handle_error(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
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
