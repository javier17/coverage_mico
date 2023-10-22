from flask import Blueprint, request
from api.src.services.sector_service import SectorService
from api.src.utils.decorators import *
from api.src.utils.utils import *

mod = Blueprint('sector_controller', __name__)
base_url = '/api/sectors'
service = SectorService


@mod.route(f'{base_url}', methods=['GET'])
@handle_error
def get_all():
    return service.get_all()


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
def get_by_id(model_id):

    return service.get_by_id(model_id)