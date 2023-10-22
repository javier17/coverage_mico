FROM python:3.11.3

COPY . ./app/micro_users
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 5002
ENV PYTHONPATH=/app
ENV FLASK_APP=/main.py
CMD ["python", "/app/micro_users/src/main.py"]