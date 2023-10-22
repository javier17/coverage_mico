import os


class BaseConfig(object):
    # postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
    _db_type = os.environ.get("DB_TYPE", default="sqlite")
    _db_user = os.environ.get("DB_USER", default="/development.db")
    _db_password = os.environ.get("DB_PASSWORD", default="")
    _db_host = os.environ.get("DB_HOST", default="")
    _db_port = os.environ.get("DB_PORT", default="")
    _db_name = os.environ.get("DB_NAME", default="")

    if _db_type !='sqlite':
        SQLALCHEMY_DATABASE_URI = f'{_db_type}://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}'
    else:
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite'

    print(SQLALCHEMY_DATABASE_URI)
    SECURITY_SERVICE = os.environ.get("SECURITY_SERVICE", default="http://localhost:5002")
    APP_PORT = os.environ.get("APP_PORT", default="3002")


class DevelopmentConfig(BaseConfig):
    DEBUG_MODE = True
    DEPLOY_MODE = True
    LOGGING_LEVEL = "DEBUG"


class UATConfig(BaseConfig):
    DEBUG_MODE = False
    DEPLOY_MODE = True
    LOGGING_LEVEL = "INFO"


class ProductionConfig(BaseConfig):
    DEBUG_MODE = False
    DEPLOY_MODE = True
    LOGGING_LEVEL = "ERROR"
