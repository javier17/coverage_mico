#!/bin/bash

# Cambia al directorio de la aplicación API
cd "./api/src"
export APP_PORT="5001"
export USER_SERVICE="http://localhost:5002"
export SECURITY_SERVICE="http://localhost:5003"
python main.py &

# Cambia al directorio del microservicio "MICRO_USERS"
cd "./micro_users/src"
export APP_PORT="5002"
export SECURITY_SERVICE="http://localhost:5003"
export DB_TYPE="sqlite"

python main.py &

# Cambia al directorio del microservicio "MICRO_AUTH"
cd "./micro_auth/src"
export APP_PORT="5003"
export JWT_SECRET_KEY="JWT_SECRET_KEY"
export DB_TYPE="sqlite"
python main.py
