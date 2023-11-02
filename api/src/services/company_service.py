import requests
import requests
from flask import current_app, request
from api.src.utils.utils import *
import json

service_path_companies = "companies"
service_path_persons = "persons"
service_path_funcionaries = "functionaries"

class CompanyService:
    def __init__(self):
        self.host = current_app.config['COMPANY_SERVICE']

    @staticmethod
    def create(data):

        host = CompanyService().host

        responseExistsCompany = requests.get(
            f"{host}/{service_path_companies}/name/{data['company']['name']}", 
            headers=request.headers)
        
        contentExistsCompany = responseExistsCompany.json()
        
        if(contentExistsCompany['status']['code'] != 200):
            return contentExistsCompany
        
        responseExistsPerson = requests.get(
            f"{host}/{service_path_persons}/email/{data['person']['email']}", 
            headers=request.headers)
        
        contentExistsPerson = responseExistsPerson.json()
        
        if(contentExistsPerson['status']['code'] != 200):
            return contentExistsPerson

        responseCompany = requests.post(
            f"{host}/{service_path_companies}", 
            headers=request.headers, 
            json=data['company'])
        

        contentCompany = responseCompany.json()

        if(contentCompany['status']['code'] != 201):
            return contentCompany
        
        responsePerson = requests.post(
            f"{host}/{service_path_persons}", 
            headers=request.headers, 
            json=data['person'])
        

        contentPerson = responsePerson.json()   

        if(contentPerson['status']['code'] != 201):
            return contentPerson

        dataF = {
            "company_id": contentCompany['response']['id'],
            "person_id": contentPerson['response']['id'],
            "rol" : data['rol']
        }

        responseFunctionary = requests.post(
            f"{host}/{service_path_funcionaries}", 
            headers=request.headers, 
            json= dataF)
        
        contentFunctionary = responseFunctionary.json()       
            
        content = responseCompany.json()

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
            f"{host}/{service_path_companies}/{id}", 
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
