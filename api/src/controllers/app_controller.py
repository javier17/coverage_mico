from flask import Blueprint
from api.src.utils.decorators import *

mod = Blueprint('app_controller', __name__)
base_url = '/api'


@mod.route(f'{base_url}/ping', methods=['GET'])
@handle_error
defs get():
    return 'pong'

