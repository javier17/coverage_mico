FROM python:3.11.3

# Copia los archivos y directorios necesarios al contenedor
COPY ./api /app/api
COPY ./micro_auth /app/micro_auth
COPY ./micro_users /app/micro_users
COPY ./requirements.txt /app/requirements.txt
COPY ./start.sh /app/start.sh

WORKDIR /app
# Instala las dependencias de Python
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003

RUN pip install -r /app/requirements.txt
RUN chmod +x /app/start.sh
ENV PYTHONPATH=/app

# Ejecuta el script de inicio
CMD ["/app/start.sh"]
