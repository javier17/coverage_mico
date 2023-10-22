from unittest import TestCase
from faker import Faker
import json
import responses
from src.utils.utils import DbService
from flask import current_app
from datetime import  datetime, timedelta
from src.controllers.users_controller import UserTools
import hashlib

def test_ping_200(client) -> None:
    solicitud_api = client.get("/app/ping",)
    response_data = solicitud_api.get_data().decode('utf-8')
    assert response_data == 'pong'

def test_create_user_201(client, base_data) -> None:
    data = []

    fake = Faker()
    email = fake.email()
    fullname = fake.name()
    phone = fake.phone_number()
    country = fake.country()
    password = fake.password(length=12)

    data = {
        "fullname": fullname,
        "phone": phone,
        "email": email,
        "password": password,
        "country": country
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print('--------------------')
    print(response)
    assert response['status']['code'] == 201

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


@responses.activate
def test_get_by_id_200(client, base_data) -> None:
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

    headers = {'Content-Type': 'application/json'}
    request = client.get("/users/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200


@responses.activate
def test_delete_by_id_204(client, base_data) -> None:
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

    headers = {'Content-Type': 'application/json'}
    request = client.delete("/users/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 204


@responses.activate
def test_get_all_id_200(client, base_data) -> None:
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

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users/filter", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200


@responses.activate
def test_update_by_id_200(client, base_data) -> None:
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

    data = {
        "email" : 'javier@gmail.com',
        "username": "Javier"
    }    

    headers = {'Content-Type': 'application/json'}
    request = client.put("/users/1", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200


@responses.activate
def test_password_404(client, base_data) -> None:
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

    data = {
        "password" : 'password1',
        "new_password": "passwor2"
    }    

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users/password", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 404



def test_check_user_name_valid():
    valid_names = ["ExampleCompany", "MyCompany"]
    for name in valid_names:
        result = UserTools.check_username(name)
        print(result)
        assert result == True

def test_check_user_name_invalid():
    valid_names = ["Example Company", "MyCompany 12"]
    for name in valid_names:
        result = UserTools.check_username(name)
        print(result)
        assert result == False


def test_check_pasword():
    class User:
        def __init__(self, salt, password):
            self.salt = salt
            self.password = password

    user = User("somesalt", hashlib.sha256("correctpasswordsomesalt".encode()).hexdigest())

    result = UserTools.check_password(user, "correctpassword")
    assert result == True



def test_valid_email():
    # Prueba con una dirección de correo electrónico válida
    result = UserTools.check_email("example")
    assert result == False


def test_create_user_invalid_email_412(client, base_data) -> None:
    data = []

    fake = Faker()
    email = "javier"
    fullname = fake.name()
    phone = fake.phone_number()
    country = fake.country()
    password = fake.password(length=12)

    data = {
        "fullname": fullname,
        "phone": phone,
        "email": email,
        "password": password,
        "country": country
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print('--------------------')
    print(response)
    assert response['status']['code'] == 412



def test_create_user_already_exists_412(client, base_data) -> None:
    data = []

    fake = Faker()
    email = fake.email()
    fullname = fake.name()
    phone = fake.phone_number()
    country = fake.country()
    password = fake.password(length=12)

    data = {
        "fullname": fullname,
        "phone": phone,
        "email": email,
        "password": password,
        "country": country
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users", data=json.dumps(data), headers=headers)
    request2 = client.post("/users", data=json.dumps(data), headers=headers)
    response2 = json.loads(request2.get_data())
    print('--------------------')
    print(response2)
    assert response2['status']['code'] == 412


@responses.activate
def test_get_all_id_unauthirized_5000(client, base_data) -> None:

    headers = {'Content-Type': 'application/json'}
    request = client.post("/users/filter", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 500



@responses.activate
def test_password_412(client, base_data) -> None:
    x = base_data[0]
    print('=========')
    print(x)
    print('=========')
    tamaño = len(base_data)
    print("El tamaño de la lista es:", tamaño)
    base_data[0]["password"]
    print(base_data[0]["password"])
    print('=========')
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


    data = {
        "id": 1,
        "password" : base_data[0]["password"],
        "new_password": "a123"
    }    


    headers = {'Content-Type': 'application/json'}
    request = client.post("/users/password", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200
