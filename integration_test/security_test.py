import os
from flask import Flask, request, jsonify
import requests
from faker import Faker
import time

app = Flask(__name__)

# Obtener la URL del endpoint de inicio de sesión desde una variable de entorno
login_endpoint = os.environ.get("LOGIN_ENDPOINT")

# Obtener la URL del endpoint de consulta de información del usuario desde una variable de entorno
user_info_endpoint = os.environ.get("USER_INFO_ENDPOINT")

# Conjunto de datos de usuarios válidos (usuario: contraseña)
valid_users = {
    "superadmin": "superadmin123*",
    "usersadmin": "usersadmin123*",
    "usersreadonly": "usersreadonly123*",
    "permissionsadmin": "permissionsadmin123*",
    "permissionsreadonly": "permissionsreadonly123*",
    "rolsadmin": "rolsadmin123*",
    "rolsreadonly": "rolsreadonly123*",
}

fake = Faker()

# Método para intentar conectarse al endpoint de consulta de usuarios con tokens inválidos generados por Faker
def test_invalid_token(num_tests): 

    test_results = []

    for _ in range(num_tests):
        invalid_token = fake.uuid4()  # Genera un token inválido con Faker

        # Mide el tiempo de inicio de la prueba
        start_time = time.time()

        # Realiza una solicitud para consultar la información del usuario con un token inválido
        user_info_response = simulate_user_info_request(invalid_token, 1)
        user_info_response_code = user_info_response.json().get('status')['code']

        # Mide el tiempo de finalización de la prueba
        end_time = time.time()

        # Calcula el tiempo de respuesta de la prueba
        response_time = end_time - start_time

        # Comprueba si la prueba fue exitosa (esperas que falle)
        test_passed = user_info_response_code != 200

        # Registra el resultado de la prueba con token inválido y su tiempo de respuesta
        test_result = {
            "response_code": user_info_response_code,
            "test_passed": test_passed,
            "response_time": response_time  # Tiempo de respuesta de la prueba
        }
        
        test_results.append(test_result)

    # Regresa el resultado de todas las pruebas realizadas
    return test_results


# Método para realizar pruebas de autorización con usuarios válidos
def test_success_scenario():
    test = []

    # Itera a través de los usuarios válidos y realiza pruebas de autorización
    for username, password in valid_users.items():
        # Realiza una solicitud de inicio de sesión para obtener el token
        start_time_login = time.time()  # Registra el tiempo de inicio
        login_response = simulate_login(username, password)
        end_time_login = time.time()  # Registra el tiempo de finalización
        login_response_code = login_response.status_code
        user_id = login_response.json().get("response")['id']
        refresh_token = login_response.json().get("response")['refresh_token']

        # Realiza una solicitud para consultar la información del usuario
        start_time_user_request = time.time()  # Registra el tiempo de inicio
        user_info_response = simulate_user_info_request(refresh_token, user_id)
        end_time_user_request = time.time()  # Registra el tiempo de finalización
        user_info_response_code = user_info_response.status_code

        # Calcula el tiempo de respuesta para cada solicitud
        login_response_time = end_time_login - start_time_login
        user_request_response_time = end_time_user_request - start_time_user_request

        # Comprueba si la prueba fue exitosa
        test_passed = login_response_code == 200 and user_info_response_code == 200

        # Registra el resumen de la prueba
        test.append({
            "response_code_login": login_response_code,
            "response_code_user_request": user_info_response_code,
            "test_passed": test_passed,
            "login_response_time": login_response_time,
            "user_request_response_time": user_request_response_time
        })

    return test

# Método para realizar pruebas de autorización con usuarios aleatorios generados por Faker
def test_random_users(num_users):
    test = []

    for _ in range(num_users):
        # Genera datos aleatorios utilizando Faker
        fake_username = fake.user_name()
        fake_password = fake.password()

        # Realiza una solicitud de inicio de sesión para obtener el token
        start_time_login = time.time()  # Registra el tiempo de inicio
        login_response = simulate_login(fake_username, fake_password)
        end_time_login = time.time()  # Registra el tiempo de finalización
        login_response_code = login_response.json().get('status')['code']

        # Calcula el tiempo de respuesta para la solicitud de inicio de sesión
        login_response_time = end_time_login - start_time_login

        # Comprueba si la prueba fue exitosa
        test_passed = login_response_code != 200

        # Registra el resumen de la prueba
        test.append({
            "fake_username": fake_username,
            "fake_password": fake_password,
            "response_code_login": login_response_code,
            "test_passed": test_passed,
            "login_response_time": login_response_time
        })

    return test

# Endpoint para realizar pruebas de autorización
@app.route('/test_authorization', methods=['GET'])
def test_authorization():
    # Realiza pruebas de usuarios válidos
    valid_users_test = test_success_scenario()

    # Realiza pruebas de usuarios aleatorios generados por Faker (10 usuarios en este ejemplo)
    random_users_test = test_random_users(10)
    invalid_token_test = test_invalid_token(10)

    # Calcula el número de pruebas aprobadas y el número de pruebas totales para ambos conjuntos de pruebas
    num_valid_users_tests_approved = sum(test['test_passed'] for test in valid_users_test)
    num_random_users_tests_approved = sum(test['test_passed'] for test in random_users_test)
    num_invalid_token_test_approved = sum(test['test_passed'] for test in invalid_token_test)
    num_valid_users_tests_total = len(valid_users_test)
    num_random_users_tests_total = len(random_users_test)
    num_invalid_token_test_total = len(invalid_token_test)

    # Encuentra la solicitud con el mayor y el menor tiempo de respuesta para usuarios válidos
    valid_users_test.sort(key=lambda x: x["login_response_time"])
    fastest_valid_user_request = valid_users_test[0]
    slowest_valid_user_request = valid_users_test[-1]

    # Encuentra la solicitud con el mayor y el menor tiempo de respuesta para usuarios aleatorios
    random_users_test.sort(key=lambda x: x["login_response_time"])
    fastest_random_user_request = random_users_test[0]
    slowest_random_user_request = random_users_test[-1]

    invalid_token_test.sort(key=lambda x: x["response_time"])
    fastest_invalid_token_test_request = invalid_token_test[0]
    slowest_invalid_token_test_request = invalid_token_test[-1]

    # Genera un resumen de los resultados
    result_summary = {
        "valid_users_test_summary": {
            "test_approved": num_valid_users_tests_approved,
            "test_total": num_valid_users_tests_total,
            "test_failed": num_valid_users_tests_total - num_valid_users_tests_approved,
            "executed_tests": valid_users_test,
            "fastest_request": fastest_valid_user_request,
            "slowest_request": slowest_valid_user_request
        },
        "random_users_test_summary": {
            "test_approved": num_random_users_tests_approved,
            "test_total": num_random_users_tests_total,
            "test_failed": num_random_users_tests_total - num_random_users_tests_approved,
            "executed_tests": random_users_test,
            "fastest_request": fastest_random_user_request,
            "slowest_request": slowest_random_user_request
        },
        "invalid_token_test_summary": {
            "test_approved": num_invalid_token_test_approved,
            "test_total": num_invalid_token_test_total,
            "test_failed": num_invalid_token_test_total - num_invalid_token_test_approved,
            "executed_tests": invalid_token_test,
            "fastest_request": fastest_invalid_token_test_request,
            "slowest_request": slowest_invalid_token_test_request
        },
    }

    return jsonify(result_summary)

# Realiza una solicitud de inicio de sesión a un endpoint real
def simulate_login(username, password):
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(login_endpoint, json=data)
    return response

# Realiza una solicitud para consultar la información del usuario a un endpoint real
def simulate_user_info_request(token, id):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{user_info_endpoint}/{id}", headers=headers)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('APP_PORT', '3000'))
