import os

from flask import Flask

from api.src.controllers.app_controller import mod as app_blueprint
from api.src.controllers.auth_controller import mod as auth_blueprint
from api.src.controllers.user_controller import mod as users_blueprint

from api.src.controllers.sector_controller import mod as sector_blueprint
from api.src.controllers.company_controller import mod as company_blueprint



def create_app(flaskname):
    _deployed_env_ = os.environ.get("ENVIRONMENT", default="development")
    app = Flask(__name__)

    app.register_blueprint(users_blueprint)
    app.register_blueprint(app_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(sector_blueprint)
    app.register_blueprint(company_blueprint)

    if (_deployed_env_ == 'development'):
        app.config.from_object('api.src.configuration.DevelopmentConfig')
    elif (_deployed_env_ == 'uat'):
        app.config.from_object('api.src.configuration.UATConfig')
    else:
        app.config.from_object('api.src.configuration.ProductionConfig')

    return app
