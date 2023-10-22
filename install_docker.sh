#!/bin/bash

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker no está instalado. Instalando Docker..."
    
    # Actualizar los paquetes del sistema
    sudo yum update -y  # Para Amazon Linux 2 o CentOS
    # o
    # sudo apt-get update -y  # Para Ubuntu

    # Instalar las dependencias necesarias
    sudo yum install -y docker  # Para Amazon Linux 2 o CentOS
    # o
    # sudo apt-get install -y docker.io  # Para Ubuntu

    # Iniciar y habilitar el servicio Docker
    sudo systemctl start docker
    sudo systemctl enable docker

    # Agregar el usuario al grupo "docker"
    sudo usermod -aG docker $USER

    echo "Docker ha sido instalado. Por favor, inicia sesión nuevamente para aplicar los cambios."
    exit 1
else
    echo "Docker ya está instalado."
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose no está instalado. Instalando Docker Compose..."

    # Descargar la última versión de Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

    # Dar permisos de ejecución al archivo descargado
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose ha sido instalado."
else
    echo "Docker Compose ya está instalado."
fi

# Mostrar la versión de Docker y Docker Compose
docker --version
docker-compose --version

echo "Proceso de verificación e instalación completado."
