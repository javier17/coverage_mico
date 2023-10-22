
import requests
from flask import current_app

class SecurityService:

    def __init__(self):
        self.host = current_app.config['SECURITY_SERVICE']


    @staticmethod
    def generate_token(user):

        host = SecurityService().host

        data = {
            'id': user['id'], 
            'email': user['email']
        }
        response = requests.post(
            f"{host}/auth/token", json=data)
        content = response.json()
        return content["response"]
    

    @staticmethod
    def get_tokendata(request):

        host = SecurityService().host
        response = requests.get(
            f"{host}/auth/me", headers=request.headers)
        content = response.json()
        return content["response"]
  