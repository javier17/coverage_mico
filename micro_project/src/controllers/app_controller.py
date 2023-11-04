from flask import Blueprint
from micro_project.src.utils.decorators import handle_error

mod = Blueprint('app_controller', __name__)
base_url = '/projects'

@mod.route(f'{base_url}/ping', methods=['GET'])
@handle_error
def get():
    return 'pong'
 