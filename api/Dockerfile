FROM python:3.11.3

COPY . ./app/api
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 5001
ENV PYTHONPATH=/app
ENV FLASK_APP=/main.py
ENV ENVIRONMENT=uat


CMD ["python", "/app/api/src/main.py"]