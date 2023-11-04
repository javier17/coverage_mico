import hashlib
import re
from datetime import datetime, timedelta
import json
import jwt
import bcrypt

from flask import Blueprint, request

from micro_project.src.models.models import Project, ProjectShema , Profile, ProfileShema, Functionary, db
from micro_project.src.utils.decorators import handle_error, authorizer, validate_required_fields
from micro_project.src.utils.utils import ResponseTools, DbService
from micro_project.src.services.security import SecurityService


mod = Blueprint('project_controller',__name__)
model_schema = ProjectShema()
base_url = '/projects'
entity = Project

@mod.route(f'{base_url}', methods=['POST'])
@handle_error
@authorizer()
@validate_required_fields(['name', 'description', 'status', 'rolProject'])
def create():

    data = SecurityService.get_tokendata(request)

    c_name = request.json['name']
    c_description = request.json['description']
    c_status = request.json['status']
    c_rol_project =  request.json['rolProject']


    if not (ProjectTools.check_name(c_name)):
        message = 'Invalid name'
        return ResponseTools.build_response(code=412, message=message)

    company = entity.query.filter((
        entity.name.ilike(c_name))).first()
    
    if company:
        message = 'The project name entered already exists'
        return ResponseTools.build_response(code=412, message=message)

    company = Functionary.query.filter_by(person_id = (data['id'])).first()

    project = Project(name = c_name, description = c_description, status = c_status, company_id = company.company_id)

    profile = Profile(name= c_rol_project, project=project)

    db.session.add(project)
    db.session.add(profile)

    db.session.commit()

    aux = entity.query.filter((
        entity.name.ilike(c_name))).first()
    
    json_data = {"_select_fields": [
        "id", "name", "description", "status", "profile"]}
    responseProject = DbService.db_generic_get_by_id(
            model_class=entity, model_id=aux.id, json_data=json_data)
    
    response = {
        "response": {
            "id": responseProject['response']['id'],
            "name": responseProject['response']['name'],
            "description": responseProject['response']['description'], 
            "status": responseProject['response']['status'], 
            "profile": responseProject['response']['profile']            
        },
        "status": {
            "code": 201,
            "errorMessage": None,
            "message": "Project created successfully",
            "type": "success"
        }
    }

    return response



@mod.route(f'{base_url}/<int:model_id>', methods=['DELETE'])
@handle_error
@authorizer()
def delete(model_id):
    return DbService.db_generic_delete(model_id, Project)



@mod.route(f'{base_url}/<int:model_id>', methods=['PUT'])
@handle_error
@authorizer()
@validate_required_fields(['name', 'description', 'status'])
def update(model_id):
    response = DbService.db_generic_update(model_id, request.json, Project)
    response['response'] = {key: value for key, value in response['response'].items(
    )}
    return response


@mod.route(f'{base_url}', methods=['GET'])
@handle_error
@authorizer()
def getAll():

    data = SecurityService.get_tokendata(request)   

    company = Functionary.query.filter_by(person_id = (data['id'])).first()

    filters = {
        "_filters" : {
            "company_id": company.company_id
        }
    }
    response = DbService.db_generic_get(Project, filters)
    return response




class ProjectTools:
    def check_name(name):
        #regex = r'^[a-zA-Z0-9_.- ]{3,32}$'
        regex = r'^[a-zA-Z0-9_. -]{3,32}$'
        if (re.match(regex, name)):
            return True
        else:
            return False
        
