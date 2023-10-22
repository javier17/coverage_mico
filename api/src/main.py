

import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from api.src import create_app

app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)
cors_origins = os.environ.get(
    'CORS_ORIGINS', 'http://localhost:4200').split(',')
cors = CORS(app, origins=cors_origins, supports_credentials=True)


print('inicio api')
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,
            port=os.environ.get('APP_PORT', '5001'))
