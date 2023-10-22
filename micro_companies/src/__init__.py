import os 

from flask import Flask

from micro_companies.src.controllers.app_controller import mod as app_blueprint

from micro_companies.src.controllers.company_controller import mod as company_blueprint

from micro_companies.src.controllers.sector_controller import mod as sector_blueprint

from micro_companies.src.controllers.auth_controller import mod as auth_blueprint

def create_app(config_name):
    _deployed_env_ = os.environ.get("ENVIRONMENT", default="development")
    app = Flask(__name__)

    app.register_blueprint(app_blueprint)
    app.register_blueprint(company_blueprint)
    app.register_blueprint(sector_blueprint)
    app.register_blueprint(auth_blueprint)

    if (_deployed_env_ == 'development'):
        app.config.from_object(
            'micro_companies.src.configuration.DevelopmentConfig')
    elif (_deployed_env_ == 'uat'):
        app.config.from_object('micro_companies.src.configuration.UATConfig')
    else:
        app.config.from_object(
            'micro_companies.src.configuration.ProductionConfig')
    return app
