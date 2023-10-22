import os

from flask import Flask

from micro_users.src.controllers.app_controller import mod as app_blueprint
from micro_users.src.controllers.auth_controller import mod as auth_blueprint
# from micro_users.src.controllers.permissions_controller import \
#     mod as permissions_blueprint
# from micro_users.src.controllers.rols_controller import mod as rols_blueprint
from micro_users.src.controllers.users_controller import mod as users_blueprint


def create_app(config_name):
    _deployed_env_ = os.environ.get("ENVIRONMENT", default="development")
    app = Flask(__name__)

    # app.register_blueprint(permissions_blueprint)
    # app.register_blueprint(rols_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(app_blueprint)
    app.register_blueprint(auth_blueprint)

    if (_deployed_env_ == 'development'):
        app.config.from_object(
            'micro_users.src.configuration.DevelopmentConfig')
    elif (_deployed_env_ == 'uat'):
        app.config.from_object('micro_users.src.configuration.UATConfig')
    else:
        app.config.from_object(
            'micro_users.src.configuration.ProductionConfig')
    return app
