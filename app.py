from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from local_config import sql_path
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{sql_path}'
db = SQLAlchemy(app)


from views import *


api.add_resource(UserList, '/api/list/users')
api.add_resource(TaskList, '/api/list/tasks')
api.add_resource(Project, '/api/get/project')
api.add_resource(GetTask, '/api/get/task/<int:task_id>')
api.add_resource(GetUser, '/api/get/user/<int:user_id>')
api.add_resource(ChangeTask, '/api/change/task/<int:task_id>')
api.add_resource(ChangeUser, '/api/change/user/<int:user_id>')
api.add_resource(CreateTask, '/api/create/task/<int:task_id>')
api.add_resource(CreateUser, '/api/create/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)

