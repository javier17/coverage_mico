import os


class BaseConfig(object):
    PROPAGATE_EXCEPTIONS = True
    APP_PORT = os.environ.get("APP_PORT", default="3001")
    USER_SERVICE = os.environ.get("USER_SERVICE", default="")
    PRODUCT_SERVICE = os.environ.get("PRODUCT_SERVICE", default="")
    SECURITY_SERVICE = os.environ.get("SECURITY_SERVICE", default="http://localhost:5003")
    COMPANY_SERVICE = os.environ.get("COMPANY_SERVICE", default="http://localhost:5010")
    PROJECT_SERVICE = os.environ.get("PROJECT_SERVICE", default="http://localhost:5011")    


class DevelopmentConfig(BaseConfig):
    DEBUG_MODE = True
    DEPLOY_MODE = True
    LOGGING_LEVEL = "DEBUG"


class UATConfig(BaseConfig):
    DEBUG_MODE = True
    DEPLOY_MODE = False
    LOGGING_LEVEL = "INFO"


class ProductionConfig(BaseConfig):
    DEBUG_MODE = False
    DEPLOY_MODE = False
    LOGGING_LEVEL = "ERROR"

