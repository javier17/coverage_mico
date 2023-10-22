from functools import wraps
from micro_auth.src.models.models import  db
from micro_auth.src.utils.utils import *
from jwt.exceptions import ExpiredSignatureError

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

