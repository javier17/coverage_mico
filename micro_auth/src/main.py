import os
from flask_jwt_extended import JWTManager
from flask_restful import Api

from micro_auth.src import create_app
from micro_auth.src.models.models import db

# Clave secreta insegura (NO DEBERÍAS USARLA EN PRODUCCIÓN)
app = create_app('default')
app.config['SECRET_KEY'] = 'clave_insegura'
app_context = app.app_context()
app_context.push()
db.init_app(app)
try:
    db.create_all()
except:
    print('already exist')

api = Api(app)
jwt = JWTManager(app)

print('inicio auth')
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.environ.get('APP_PORT', '5003'))
