
from flask import Blueprint, request
from micro_companies.src.models.models import CompanySector, CompanySectorsShema, db
from micro_companies.src.utils.decorators import handle_error, DbService

mod = Blueprint('sector_controller', __name__)

base_url = '/sectors'
entity = CompanySector

@mod.route(f'{base_url}', methods=['GET'])
@handle_error   
def get_all():

    json_data = {"_select_fields": [
        "id", "name"]}
    response = DbService.db_generic_get(
        model_class=entity, json_data=json_data)
    return response    


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error 
def get_by_id(model_id):

    json_data = {"_select_fields": [
        "id", "name", "company_types"]}
    response = DbService.db_generic_get_by_id(
        model_class=entity, model_id=model_id, json_data=json_data)
    return response    