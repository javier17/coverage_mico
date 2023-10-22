#!/bin/bash

echo "Eliminando todos los contenedores en ejecución..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

echo "Eliminando todas las imágenes..."
docker rmi $(docker images -a -q)

echo "Eliminando todos los volúmenes..."
docker volume prune

echo "Eliminando todas las redes..."
docker network prune

echo "Limpieza completada."

PUERTOS=(5433 5434 5435 5000)  

for PUERTO in "${PUERTOS[@]}"; do
    echo "Procesando el puerto $PUERTO..."
    
    # Verifica si hay procesos en el puerto especificado
    if lsof -i :$PUERTO; then
        # Obtiene los PID de los procesos en el puerto
        PIDS=$(lsof -i :$PUERTO | awk 'NR!=1 {print $2}')
        
        # Detiene los procesos utilizando kill
        for PID in $PIDS; do
            echo "Deteniendo proceso en el puerto $PUERTO (PID $PID)..."
            kill $PID
        done
    else
        echo "No se encontraron procesos en el puerto $PUERTO."
    fi
done