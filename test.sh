#!/bin/bash

# Obtén la lista de servicios desde la variable de entorno SERVICE_LIST
SERVICES="$SERVICE_LIST"
COVERAGE=$TEST_COVERAGE

# Separa la lista de servicios en un array usando la coma como delimitador
IFS=',' read -ra SERVICE_ARRAY <<< "api"

# Variable para rastrear si hay un error
ERROR=false

# Itera sobre cada servicio y ejecuta las instrucciones
for SERVICE in "${SERVICE_ARRAY[@]}"; do
    echo "Ejecutando pruebas para el servicio $SERVICE"

    # Crea un entorno virtual de Python
    python3 -m venv venv

    # Activa el entorno virtual
    if [[ "$OSTYPE" == "msys" ]]; then
        venv\Scripts\activate
    else
        source ./venv/bin/activate
    fi
    python3.11 -m pip install --upgrade pip
    # Instala las dependencias desde requirements.txt
    pip install -r $SERVICE/requirements.txt

    # Genera un informe de cobertura y verifica la cobertura mínima
    if ! python -m coverage report -m --fail-under=90; then
        echo "La cobertura está por debajo del 80% en el servicio "$SERVICE
        exit 1
    fi
     echo "Se han ejecuta con exito los test de "$SERVICE

    # Desactiva el entorno virtual
    deactivate

done

# Verifica si hubo un error y finaliza el script con un código de salida adecuado
if [ "$ERROR" = true ]; then
    echo "¡Se encontraron errores en las pruebas!"
    exit 1
fi
