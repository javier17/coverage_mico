import requests
from flask import current_app, request
from api.src.utils.utils import *

service_path = "auth"


class AuthService:
    def __init__(self):
        self.host = current_app.config['SECURITY_SERVICE']    
    
    @staticmethod
    def refresh(headers):
        host = AuthService().host

        response = requests.get(
            f"{host}/{service_path}/refresh", 
            headers=headers)
        
        content = response.json()
        return content

    @staticmethod
    def get_token_data(headers):
        host = AuthService().host
        
        response = requests.get(
            f"{host}/{service_path}/me",
              headers=request.headers)
        
        content = response.json()
        return content.get('response')