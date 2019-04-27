from flask_restful import Resource
from models import User


class UserList(Resource):
    def get(self):
        all_users = []
        for user in User.query.all():
            all_users.append(
                { 
                    "name": user.name,
                    "assigned_tasks": user.tasks,
                    "photo_url": "static_photo.jpg"
                }
            )
        return all_users


class TaskList(Resource):
    def get(self):
        all_tasks = []
        for task in Task.query.all():
            all_tasks.append({
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "assignee": task.assignee,
                "status": task.status,
                "color": "0000ff"
            })
        return all_tasks

class Project(Resource):
    def get(self):
        project = {
            "name": "My project name",
            "description": "My project description",
            "tasks": [task.id for task in Task.query.all()],
            "users": [user.id for user in User.query.all()]
        }
        return project

class GetTask(Resource):
    def get(self, task_id):
        task = Task.query.get(int(task_id))
        ret_task = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "assignee": task.assignee,
            "status": task.status,
            "color": "0000ff"
        }
        return ret_task

class GetUser(Resource):
    def get(self, user_id):
        user = User.query.get(int(user_id))
        ret_user = {
            "name": user.name,
            "assigned_tasks": user.tasks,
            "photo_url": "static_photo.jpg"
        }
        return ret_user

class ChangeTask(Resource):
    def post(self, task_id):
        parser.add_argument('name_of_thing_you_want_to_add', type=str)
        args = parser.parse_args()

        new_task = Task()
        new_task.thing = "thing"

        db.session.add(new_task)
        db.session.commit()

        return {
            'status': True,
            'thingo' = args.get('name_of_thing_you_want_to_add')
        }
    pass

class ChangeUser(Resource):
    pass

class CreateTask(Resource):
    pass

class CreateUser(Resource):
    pass
