from flask import Blueprint
from micro_users.src.utils.decorators import *

mod = Blueprint('app_controller', __name__)
base_url = '/app'


@mod.route(f'{base_url}/ping', methods=['GET'])
@handle_error
def get():
    return 'pong'
