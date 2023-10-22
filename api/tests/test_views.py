
from unittest import TestCase
from faker import Faker
import json
import responses
from flask import current_app

def test_ping_200(client) -> None:
    solicitud_company = client.get("/api/ping",)
    response_data = solicitud_company.get_data().decode('utf-8')
    assert response_data == 'pong'


@responses.activate
def test_auth_refresh_200(client) -> None:
    responses.get(
        url=current_app.config['SECURITY_SERVICE']+'/auth/refresh',
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

    request = client.get("/api/auth/refresh", data='', headers=headers)

    response = json.loads(request.get_data())

    print(response)

    assert response['status']['code'] == 200
    assert response['response']['message'] == 'Successfully generated token'


@responses.activate
def test_create_company_201(client) -> None:
    responses.post(
        url=current_app.config['COMPANY_SERVICE']+'/companies',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "id": 1
            },
            "status": {
                "code": 201
            }
        },
        status=201
    )
    
    data = {
        "name": "Javier",
        "address": "Colombia Bogotá",
        "email": "javier@gmail.com",
        "phone": "54564",
        "sector_id": 1,
        "type_id": 1,
        "password": "a123"

    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/api/companies", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 201


@responses.activate
def test_login_company_200(client) -> None:
    responses.post(
        url=current_app.config['COMPANY_SERVICE']+'/auth/login',
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
        "address": "Colombia Bogotá",
        "password": "a123"
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/api/companies/login", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 200



@responses.activate
def test_company_get_by_id_200(client) -> None:
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
    responses.get(
        url=current_app.config['COMPANY_SERVICE']+'/companies/1',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "id": 1,
                "name": "Javier Company 20",
            },
            "status": {
                "code": 200,
                "type": "success"
            }
        },
        status=200
    )
    

    headers = {'Content-Type': 'application/json'}
    request = client.get("/api/companies/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200




@responses.activate
def test_company_get_me_200(client) -> None:
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

    responses.get(
        url=current_app.config['COMPANY_SERVICE']+'/auth/me',
        json={
            "response": {
                "email": "javier20@hotmail.com",
                "id": 1,
                "name": "Javier Company 20",
            },
            "status": {
                "code": 200,
                "type": "success"
            }
        },
        status=200
    )

    headers = {'Content-Type': 'application/json'}
    request = client.get("/api/companies/me", data='', headers=headers)
    response = json.loads(request.get_data())
    print(response)
    assert response['status']['code'] == 200


@responses.activate
def test_sector_all_200(client) -> None:
    responses.get(
        url=current_app.config['COMPANY_SERVICE']+'/sectors',
        json={
            "response": {
                "name": "Software",
                "id": 1
            },
            "status": {
                "code": 200
            }
        },
        status=200
    )

    headers = {'Content-Type': 'application/json'}
    request = client.get("/api/sectors", data='', headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 200


@responses.activate
def test_sector_By_is_200(client) -> None:
    responses.get(
        url=current_app.config['COMPANY_SERVICE']+'/sectors/1',
        json={
            "response": {
                "name": "Software",
                "id": 1
            },
            "status": {
                "code": 200
            }
        },
        status=200
    )

    headers = {'Content-Type': 'application/json'}
    request = client.get("/api/sectors/1", data='', headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 200