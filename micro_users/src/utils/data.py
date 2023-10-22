from enum import Enum
from random import choice

from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from micro_users.src.models.models import *
from micro_users.src.utils.utils import *

fake = Faker()

# Función para generar usuarios y asignar roles
def generate_users():
    if not has_records(User):
        for x in range(10):
            fk_email = fake.email()
            hashlib_password = DbTools.hash_password(f"{fk_email}123*")            
            user = User(
                fullname = fake.name(),
                phone = fake.phone_number(),
                country = fake.country(),
                email=fk_email,
                password=hashlib_password['password'],
                salt=hashlib_password['salt'],
                token=fake.random_element(),
                active=True,
                expireAt=fake.future_datetime(),
                createdAt=fake.past_datetime()
            )

            db.session.add(user)

        db.session.commit()


def has_records(model):
    return db.session.query(model).count() > 0


def init_data():
    try:
        db.create_all()
        generate_users()
    except Exception as e:
        print("already loaded",str(e))