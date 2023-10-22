import requests
import requests
from flask import current_app, request
from api.src.utils.utils import *

service_path = "companies"

class CompanyService:
    def __init__(self):
        self.host = current_app.config['COMPANY_SERVICE']


    @staticmethod
    def create(data):
        host = CompanyService().host

        response = requests.post(
            f"{host}/{service_path}", 
            headers=request.headers, 
            json=data)
            
        content = response.json()
        return content
    
    @staticmethod
    def login(data):
        host = CompanyService().host
        
        response = requests.post(
            f"{host}/auth/login", 
            json=data)
        
        content = response.json()
        return content
    
    @staticmethod
    def get_by_id(id):
        host = CompanyService().host

        response = requests.get(
            f"{host}/{service_path}/{id}", 
            headers=request.headers)
        
        content = response.json()
        return content   
    
    @staticmethod
    def get_me():
        host = CompanyService().host
        
        response = requests.get(
            f"{host}/auth/me", 
             headers=request.headers)
        
        content = response.json()
        return content
