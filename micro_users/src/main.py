

import os
from flask_restful import Api
from micro_users.src import create_app
from micro_users.src.models.models import db
from micro_users.src.utils.data import init_data

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
init_data()
api = Api(app)

print('inicio users')
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,
            port=os.environ.get('APP_PORT', '5002'))
