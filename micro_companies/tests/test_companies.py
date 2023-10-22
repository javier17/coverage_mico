from unittest.mock import patch
from faker import Faker
import json
from datetime import  datetime, timedelta
from micro_companies.src.models.models import Company
from micro_companies.src.controllers.company_controller import CompanyTools
import hashlib
import bcrypt
from flask_jwt_extended import create_access_token
from flask import current_app
import responses
from src.utils.utils import DbService


def test_ping_200(client) -> None:
    solicitud_company = client.get("/companies/ping",)
    response_data = solicitud_company.get_data().decode('utf-8')
    assert response_data == 'pong'


def test_sector_find_all_200(client, base_data):
    headers = {'Content-Type': 'application/json'}
    request = client.get("/sectors", data='', headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 200


def test_sector_find_by_id_200(client, base_data):
    headers = {'Content-Type': 'application/json'}
    request = client.get("/sectors/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200


def test_sector_find_by_id_500(client, base_data):
    headers = {'Content-Type': 'application/json'}
    request = client.get("/sectors/2", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 500


def test_create_company_201(client, base_data) -> None:
    data = []

    fake = Faker()
    name = fake.user_name()
    address = fake.street_address()

    email = fake.email()
    phone = fake.phone_number()
    location = fake.country()
    rol = fake.job()

    password = fake.password(length=12)

    expires_delta = timedelta(minutes=25)
    token = create_access_token(identity={
                                        'id':1 ,'username': name, 'email': email}, expires_delta=expires_delta)
    data.append(
        {"name": name, "email": email, "password": password,"token":token})

    salt = bcrypt.gensalt().decode()
    salted_password = password + salt
    hashlib_password = hashlib.sha256(
        salted_password.encode()).hexdigest()
            
    company = Company(name=name, address=address, email=email, phone = phone, location = location, rol = rol, sector_id= 1, type_id = 1 ,password=hashlib_password,
                salt=salt, token=token, expireAt=datetime.now(), createdAt=datetime.now()+expires_delta)

    # Convertir el objeto datetime en una cadena con un formato específico
    datetime_str = company.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    # Serializar la cadena como JSON
    json_data = json.dumps({"datetime": datetime_str})

    data = {
        "name": company.name,
        "address": company.address,
        "email": company.email,
        "phone": company.phone,
        "location": company.location,
        "rol": company.rol,
        "sector_id": company.sector_id,
        "type_id": company.type_id,
        "password": company.password,
        "salt": company.salt,
        "token": company.token,
        "expireAt": json_data,
        "createdAt": json_data
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/companies", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 201


def test_create_company_invalid_email_412(client, base_data) -> None:
    data = []

    fake = Faker()
    name = fake.user_name()
    address = fake.street_address()

    email = 'javier'
    phone = fake.phone_number()
    location = fake.country()
    rol = fake.job()

    password = fake.password(length=12)

    expires_delta = timedelta(minutes=25)
    token = create_access_token(identity={
                                        'id':1 ,'username': name, 'email': email}, expires_delta=expires_delta)
    data.append(
        {"name": name, "email": email, "password": password,"token":token})

    salt = bcrypt.gensalt().decode()
    salted_password = password + salt
    hashlib_password = hashlib.sha256(
        salted_password.encode()).hexdigest()
            
    company = Company(name=name, address=address, email=email, phone = phone, location = location ,rol = rol, sector_id= 1, type_id = 1 ,password=hashlib_password,
                salt=salt, token=token, expireAt=datetime.now(), createdAt=datetime.now()+expires_delta)

    # Convertir el objeto datetime en una cadena con un formato específico
    datetime_str = company.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    # Serializar la cadena como JSON
    json_data = json.dumps({"datetime": datetime_str})

    data = {
        "name": company.name,
        "address": company.address,
        "email": company.email,
        "phone": company.phone,
        "location": company.location,
        "rol": company.rol,
        "sector_id": company.sector_id,
        "type_id": company.type_id,
        "password": company.password,
        "salt": company.salt,
        "token": company.token,
        "expireAt": json_data,
        "createdAt": json_data
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/companies", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 412



def test_create_company_already_exists_412(client, base_data) -> None:
    data = []

    fake = Faker()
    name = fake.user_name()
    address = fake.street_address()

    email = fake.email()
    phone = fake.phone_number()
    location = fake.country()
    rol = fake.job()

    password = fake.password(length=12)

    expires_delta = timedelta(minutes=25)
    token = create_access_token(identity={
                                        'id':1 ,'username': name, 'email': email}, expires_delta=expires_delta)
    data.append(
        {"name": name, "email": email, "password": password,"token":token})

    salt = bcrypt.gensalt().decode()
    salted_password = password + salt
    hashlib_password = hashlib.sha256(
        salted_password.encode()).hexdigest()
            
    company = Company(name=name, address=address, email=email, phone = phone, location = location ,rol = rol, sector_id= 1, type_id = 1 ,password=hashlib_password,
                salt=salt, token=token, expireAt=datetime.now(), createdAt=datetime.now()+expires_delta)

    # Convertir el objeto datetime en una cadena con un formato específico
    datetime_str = company.createdAt.strftime('%Y-%m-%d %H:%M:%S')

    # Serializar la cadena como JSON
    json_data = json.dumps({"datetime": datetime_str})

    data = {
        "name": company.name,
        "address": company.address,
        "email": company.email,
        "phone": company.phone,
        "location": company.location,
        "rol": company.rol,
        "sector_id": company.sector_id,
        "type_id": company.type_id,
        "password": company.password,
        "salt": company.salt,
        "token": company.token,
        "expireAt": json_data,
        "createdAt": json_data
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/companies", data=json.dumps(data), headers=headers)
    request2 = client.post("/companies", data=json.dumps(data), headers=headers)
    response = json.loads(request2.get_data())
    assert response['status']['code'] == 412


def test_check_name_valid():
    valid_names = ["ExampleCompany", "MyCompany"]
    for name in valid_names:
        result = CompanyTools.check_name(name)
        print(result)
        assert result == True

def test_check_name_invalid():
    invalid_names = ["@Invalid Company", "TooLongCompanyNameWithInvalidCharacters!"]
    for name in invalid_names:
        result = CompanyTools.check_name(name)
        assert result == False



@responses.activate
def test_get_by_id_200(client, base_data) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/me',
        json={'id':1, 'email': "javier@hotmail.com"},
        status=200
    )

    headers = {'Content-Type': 'application/json'}
    request = client.get("/companies/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert request.status_code == 200



@responses.activate
def test_get_login_200(client, base_data) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/login',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "error": False,
                "expiration_date": "Tue, 17 Oct 2023 19:47:30 GMT",
                "id": 1,
                "message": "Successfully generated token",
                "name": "Javier Company 20",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiN2UwNzNjZTctM2EwMi00YzlhLTgzM2QtM2IyMTlmYWY2YWZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjEsImVtYWlsIjoiamF2aWVyMjBAaG90bWFpbC5jb20ifSwibmJmIjoxNjk3NTcxNTcwLCJleHAiOjE2OTc1NzIwNTB9.bSn4QTqAQNMtJ9dqrwx-wUL7lCL2NpXkVWvCvD1adH4",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg"
            },
            "status": {
                "code": 200,
                "errorMessage": '',
                "message": "Request fulfilled, document follows",
                "type": "success"
            }
        },
        status=200
    )
    responses.post(
        url=current_app.config['SECURITY_SERVICE']+'/auth/token',
        json={
            "response": {
                "expiration_date": "Tue, 17 Oct 2023 19:47:30 GMT",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiN2UwNzNjZTctM2EwMi00YzlhLTgzM2QtM2IyMTlmYWY2YWZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjEsImVtYWlsIjoiamF2aWVyMjBAaG90bWFpbC5jb20ifSwibmJmIjoxNjk3NTcxNTcwLCJleHAiOjE2OTc1NzIwNTB9.bSn4QTqAQNMtJ9dqrwx-wUL7lCL2NpXkVWvCvD1adH4",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg"
            },
            "status": {
                "code": 200,
                "errorMessage": '',
                "message": "Request fulfilled, document follows",
                "type": "success"
            }
        },
        status=200
    )

    x = base_data[1]

    data = {
        "email" : x['email'],
        "password": x['password']
    }

    print(data)

    headers = {'Content-Type': 'application/json'}
    request = client.post("/auth/login", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print('--------------------')
    print(response)
    print('--------------------')
    assert response['status']['code'] == 200
    assert response['response']['message'] == 'Successfully generated token'


@responses.activate
def test_get_auth_me_200(client, base_data) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/login',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "error": False,
                "expiration_date": "Tue, 17 Oct 2023 19:47:30 GMT",
                "id": 1,
                "message": "Successfully generated token",
                "name": "Javier Company 20",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiN2UwNzNjZTctM2EwMi00YzlhLTgzM2QtM2IyMTlmYWY2YWZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjEsImVtYWlsIjoiamF2aWVyMjBAaG90bWFpbC5jb20ifSwibmJmIjoxNjk3NTcxNTcwLCJleHAiOjE2OTc1NzIwNTB9.bSn4QTqAQNMtJ9dqrwx-wUL7lCL2NpXkVWvCvD1adH4",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg"
            },
            "status": {
                "code": 200,
                "errorMessage": '',
                "message": "Request fulfilled, document follows",
                "type": "success"
            }
        },
        status=200
    )
    responses.post(
        url=current_app.config['SECURITY_SERVICE']+'/auth/token',
        json={
            "response": {
                "expiration_date": "Tue, 17 Oct 2023 19:47:30 GMT",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiN2UwNzNjZTctM2EwMi00YzlhLTgzM2QtM2IyMTlmYWY2YWZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjEsImVtYWlsIjoiamF2aWVyMjBAaG90bWFpbC5jb20ifSwibmJmIjoxNjk3NTcxNTcwLCJleHAiOjE2OTc1NzIwNTB9.bSn4QTqAQNMtJ9dqrwx-wUL7lCL2NpXkVWvCvD1adH4",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg"
            },
            "status": {
                "code": 200,
                "errorMessage": '',
                "message": "Request fulfilled, document follows",
                "type": "success"
            }
        },
        status=200
    )
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/me',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "error": False,
                "expiration_date": "Tue, 17 Oct 2023 19:47:30 GMT",
                "id": 1,
                "message": "Successfully generated token",
                "name": "Javier Company 20",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiN2UwNzNjZTctM2EwMi00YzlhLTgzM2QtM2IyMTlmYWY2YWZlIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjEsImVtYWlsIjoiamF2aWVyMjBAaG90bWFpbC5jb20ifSwibmJmIjoxNjk3NTcxNTcwLCJleHAiOjE2OTc1NzIwNTB9.bSn4QTqAQNMtJ9dqrwx-wUL7lCL2NpXkVWvCvD1adH4",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg"
            },
            "status": {
                "code": 200,
                "errorMessage": '',
                "message": "Request fulfilled, document follows",
                "type": "success"
            }
        },
        status=200
    )    

    x = base_data[1]

    data = {
        "email" : x['email'],
        "password": x['password']
    }

    print(data)

    headers = {'Content-Type': 'application/json'}
    request = client.get("/auth/me", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print('----------REPONSE----------')
    print(response)
    print('--------------------')
    assert response['message'] == 'Successfully generated token'


@responses.activate
def test_get_login_missing_password_400(client, base_data) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/login',
        json={'id':1},
        status=404
    )

    x = base_data[1]

    data = {
        "email" : x['email']
    }


    headers = {'Content-Type': 'application/json'}
    request = client.post("/auth/login", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 400
    assert response['status']['message'] == 'Missing required fields: password'


def test_get_login_missing_login_400(client, base_data) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/login',
        status=400
    )

    x = base_data[1]

    data = {
        "email" : x['email']
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/auth/login", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 400
    assert response['status']['message'] == 'Missing required fields: password'



