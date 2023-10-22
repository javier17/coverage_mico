import requests
import requests
from flask import current_app, request
from api.src.utils.utils import *

service_path = 'sectors'

class SectorService:
    def __init__(self):
        self.host = current_app.config['COMPANY_SERVICE']


    @staticmethod
    def get_all():
        host = SectorService().host

        response = requests.get(
            f"{host}/{service_path}", 
            headers=request.headers, 
        )
            
        content = response.json()
        return content


    @staticmethod
    def get_by_id(id):
        host = SectorService().host

        response = requests.get(
            f"{host}/{service_path}/{id}", 
            headers=request.headers)
            
        content = response.json()
        return content    
