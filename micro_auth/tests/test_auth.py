import json
from unittest.mock import patch

def test_ping_200(client) -> None:
    solicitud_company = client.get("/app/ping",)
    response_data = solicitud_company.get_data().decode('utf-8')
    assert response_data == 'pong'


def test_create_token_200(client) -> None:
    headers = {'Content-Type': 'application/json'}
    data = {
        "email" : 'email',
        "password": 'password'
    }
    request = client.post("/auth/token", data=json.dumps(data), headers=headers)

    print(request)
    response = json.loads(request.get_data())

    print(response)

    assert response['status']['code'] == 200


def test_refresh_token_500(client) -> None:
    headers = {'Content-Type': 'application/json'}

    request = client.get("/auth/refresh", data='', headers=headers)

    print(request)
    response = json.loads(request.get_data())

    print(response)

    assert response['status']['code'] == 500


def test_refresh_token_401(client) -> None:
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {''}"
        }

    request = client.get("/auth/refresh", data='', headers=headers)

    print(request)
    response = json.loads(request.get_data())

    print(response)

    assert response['status']['code'] == 401
    assert response['status']['message'] == 'Invalid refresh token'




def test_refresh_token_signature_has_expired_401(client, base_data) -> None:
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg'}"
        }

    request = client.get("/auth/refresh", data='', headers=headers)

    response = json.loads(request.get_data())

    assert response['status']['code'] == 401
    assert response['status']['errorMessage'] == 'Signature has expired'
    assert response['status']['message'] == 'Failed authentication'



def test_auth_me_signature_has_expired_401(client, base_data) -> None:
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg'}"
        }

    request = client.get("/auth/me", data='', headers=headers)

    response = json.loads(request.get_data())

    assert response['status']['code'] == 401
    assert response['status']['errorMessage'] == 'Signature has expired'
    assert response['status']['message'] == 'Failed authentication'


def test_auth_me_invalid_refresh_token_401(client, base_data) -> None:
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {'sImlhdCI6MTY5NzU3MTU3MCwianRpIjoiYTk5YTY0ODktODRhOC00YzBmLTliOTEtNGI0MWRlZjc1NDEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImlkXCI6IDEsIFwiZW1haWxcIjogXCJqYXZpZXIyMEBob3RtYWlsLmNvbVwifSIsIm5iZiI6MTY5NzU3MTU3MCwiZXhwIjoxNjk3NTcxOTMwfQ.1Aw-lWjHQ5mTr2J6lGTNr2HOw0n3XTBSM_s-gT0QSTg'}"
        }

    request = client.get("/auth/me", data='', headers=headers)

    response = json.loads(request.get_data())

    assert response['status']['code'] == 401
    assert response['status']['message'] == 'Invalid refresh token'


