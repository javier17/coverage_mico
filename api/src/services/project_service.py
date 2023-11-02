import requests
from flask import current_app, request
from api.src.utils.utils import *

service_path_projects = "projects"


class ProjectService:
    def __init__(self):
        self.host = current_app.config['PROJECT_SERVICE']

    @staticmethod
    def create(data):
        host = ProjectService().host

        response = requests.post(
            f"{host}/{service_path_projects}", 
            headers=request.headers, 
            json=data)        
        
        content = response.json()
        return content
    
    @staticmethod
    def update(id, data):
        host = ProjectService().host

        response = requests.put(
            f"{host}/{service_path_projects}/{id}", 
            json=data, 
            headers=request.headers)
        
        content = response.json()
        return content    
    
    @staticmethod
    def delete(id):
        host = ProjectService().host

        response = requests.delete(
            f"{host}/{service_path_projects}/{id}", 
            headers=request.headers)
        
        content = response.json()
        return content    

    @staticmethod
    def get_all():
        host = ProjectService().host

        response = requests.get(
            f"{host}/{service_path_projects}", 
            headers=request.headers)

        content = response.json()

        return content   
