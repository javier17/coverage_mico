import requests
from flask import current_app, request
from api.src.utils.utils import *

service_path = "users"


class UserService:
    def __init__(self):
        self.host = current_app.config['USER_SERVICE']

    @staticmethod
    def create(data):
        host = UserService().host

        response = requests.post(
            f"{host}/{service_path}", 
            headers=request.headers, 
            json=data)
        
        content = response.json()
        return content
    
    @staticmethod
    def password(data):
        host = UserService().host

        response = requests.post(
            f"{host}/{service_path}/password", 
            headers=request.headers, 
            json=data)
        
        content = response.json()
        return content

    @staticmethod
    def update(id, data):
        host = UserService().host

        response = requests.put(
            f"{host}/{service_path}/{id}", 
            json=data, 
            headers=request.headers)
        
        content = response.json()
        return content

    @staticmethod
    def delete(id):
        host = UserService().host

        response = requests.delete(
            f"{host}/{service_path}/{id}", 
            headers=request.headers)
        
        content = response.json()
        return content

    @staticmethod
    def get_by_id(id):
        host = UserService().host

        response = requests.get(
            f"{host}/{service_path}/{id}", 
            headers=request.headers)
        
        content = response.json()
        return content    

    @staticmethod
    def get_all(data):
        host = UserService().host

        response = requests.post(
            f"{host}/{service_path}/all", 
            headers=request.headers, 
            json=data)
        
        content = response.json()
        return content

    @staticmethod
    def login(data):
        host = UserService().host
        
        response = requests.post(
            f"{host}/auth/login", 
            json=data)
        
        content = response.json()
        return content
