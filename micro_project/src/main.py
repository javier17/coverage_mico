import os
from flask_restful import Api
from micro_project.src import create_app
from micro_project.src.models.models import db


app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
try:
    db.create_all()
except:
    print('already exist')
api = Api(app)

print('inicio Micro Project')
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,
            port=os.environ.get('APP_PORT', '5011'))
 