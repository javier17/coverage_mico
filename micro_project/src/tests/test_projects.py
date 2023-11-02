from faker import Faker
import json
import responses
from flask import current_app
from micro_project.src.controllers.project_controller import ProjectTools

def test_ping_200(client) -> None:
    solicitud_company = client.get("/projects/ping",)
    response_data = solicitud_company.get_data().decode('utf-8')
    assert response_data == 'pong'

@responses.activate
def test_create_project_201(client, base_data) -> None:
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

    data = []

    fake = Faker()    

    name = fake.company_suffix()
    description = fake.paragraph(nb_sentences=2)
    status = "Activo"

    data = {
        "name": name,
        "description": description,
        "status": status,
        "rolProject": "Analista Senior"
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/projects", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 201



@responses.activate
def test_delete_project_204(client, base_data) -> None:
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
    request = client.delete("/projects/1", data='', headers=headers)
    response = json.loads(request.get_data())
    print(request)
    print(response)
    assert response['status']['code'] == 204


@responses.activate
def test_delete_project_200(client, base_data) -> None:
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
        "name": 'Name update',
        "description": 'description update',
        "status": 'status update'
    }

    headers = {'Content-Type': 'application/json'}
    request = client.put("/projects/1", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())

    assert response['status']['code'] == 200


@responses.activate
def test_get_all_200(client, base_data) -> None:
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
    request = client.get("/projects", data='', headers=headers)
    response = json.loads(request.get_data())

    assert response['status']['code'] == 200



def test_check_name_invalid():
    invalid_names = ["@Invalid Company", "TooLongCompanyNameWithInvalidCharacters!"]
    for name in invalid_names:
        result = ProjectTools.check_name(name)
        assert result == False



@responses.activate
def test_create_project_name_invalid_412(client, base_data) -> None:
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

    data = []

    fake = Faker()    

    name = 'Empresa $%&@- '
    description = fake.paragraph(nb_sentences=2)
    status = "Activo"

    data = {
        "name": name,
        "description": description,
        "status": status,
        "rolProject": "Analista Senior"
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/projects", data=json.dumps(data), headers=headers)
    response = json.loads(request.get_data())
    assert response['status']['code'] == 412



@responses.activate
def test_create_project_company_exists_412(client, base_data) -> None:
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

    data = []

    fake = Faker()    

    name = 'Compania'
    description = fake.paragraph(nb_sentences=2)
    status = "Activo"

    data = {
        "name": name,
        "description": description,
        "status": status,
        "rolProject": "Analista Senior"
    }

    headers = {'Content-Type': 'application/json'}
    request = client.post("/projects", data=json.dumps(data), headers=headers)

    request2 = client.post("/projects", data=json.dumps(data), headers=headers)

    response2 = json.loads(request2.get_data())

    print('----------------------------')
    print(response2)
    print('----------------------------')

    assert response2['status']['code'] == 412    