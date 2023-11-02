import os 

from flask import Flask

from micro_project.src.controllers.app_controller import mod as app_blueprint

from micro_project.src.controllers.project_controller import mod as project_blueprint



def create_app(config_name):
    _deployed_env_ = os.environ.get("ENVIRONMENT", default="development")
    app = Flask(__name__)

    app.register_blueprint(app_blueprint)
    app.register_blueprint(project_blueprint)


    if (_deployed_env_ == 'development'):
        app.config.from_object(
            'micro_project.src.configuration.DevelopmentConfig')
    elif (_deployed_env_ == 'uat'):
        app.config.from_object('micro_project.src.configuration.UATConfig')
    else:
        app.config.from_object(
            'micro_project.src.configuration.ProductionConfig')
    return app
