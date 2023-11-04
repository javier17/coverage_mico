from datetime import datetime

from flask import Blueprint, request
from micro_auth.src.models.models import RefreshToken, RefreshTokenSchema
from micro_auth.src.utils.decorators import handle_error
from micro_auth.src.utils.utils import DbService, SecurityTools, ResponseTools

mod = Blueprint('auth_controller', __name__)
model_schema = RefreshTokenSchema()
base_url = '/auth'
entity = RefreshToken


@mod.route(f'{base_url}/<int:model_id>', methods=['GET'])
@handle_error
def get_by_id(model_id):

    json_data = {"_select_fields": [
        "id", "rols", 'username']}
    response = DbService.db_generic_get_by_id(
        model_class=entity, model_id=model_id, json_data=json_data)
    return response



@mod.route(f'{base_url}/<int:model_id>', methods=['DELETE'])
@handle_error
def delete(model_id):

    return DbService.db_generic_delete(model_id, entity)

@mod.route(f'{base_url}/token', methods=['POST'])
@handle_error
def create_token():   
    #Eliminar tokens vencidos    
    date_now=datetime.now()
    DbService.clean_expired_tokens('')  
    
    #Generrar tokens
    user_data =request.json
    if user_data:

        new_refresh_token = SecurityTools.generate_refresh_token(user_data)  
        new_token = SecurityTools.generate_token(user_data)

        data = {"token":new_refresh_token[0],"expiration_date":date_now + new_refresh_token[1]}   

    DbService.db_generic_create(data= data, model_class=entity)
    response={"token":new_token,"refresh_token":new_refresh_token[0],"expiration_date":date_now + new_refresh_token[1]} 
  
    return ResponseTools.build_response(response=response,code=200)

@mod.route(f'{base_url}/refresh', methods=['GET'])
@handle_error
def refresh_token():   

    #Eliminar tokens vencidos    
    DbService.clean_expired_tokens('')  
    date_now=datetime.now()

    #validar token
    old_refresh_token = request.headers.environ['HTTP_AUTHORIZATION'].split("Bearer ")[1]    
    refresh_token = RefreshToken.query.filter_by(token=old_refresh_token).first() 

    if not refresh_token:
        return ResponseTools.build_response(message="Invalid refresh token",code=401)
    
    #Generar nuevo token
    token_data =SecurityTools.get_tokendata(request)    
    new_refresh_token = SecurityTools.generate_refresh_token(token_data)  

    data = {"token":new_refresh_token[0],"expiration_date":date_now + new_refresh_token[1]}
    response = {"refresh_token":new_refresh_token[0],"expiration_date":date_now + new_refresh_token[1]}

    DbService.db_generic_create(data= data, model_class=entity)
    return ResponseTools.build_response(response=response,code=200)




@mod.route(f'{base_url}/me', methods=['GET'])
@handle_error
def get_me():
    DbService.clean_expired_tokens('')  
    
    #validar token
    old_refresh_token = request.headers.environ['HTTP_AUTHORIZATION'].split("Bearer ")[1]
    refresh_token = RefreshToken.query.filter_by(token=old_refresh_token).first() 

    if not refresh_token:
        return ResponseTools.build_response(message="Invalid refresh token",code=401)
    
 
    token_data = SecurityTools.get_tokendata(request)
    return ResponseTools.build_response(response=token_data)