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
            all_tasks.append(
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "assignee": task.assignee,
                "status": task.status,
                "color": "0000ff"
            )
        return all_tasks

class Project(Resource):
    def get(self):
        project = {
            "name": "My project name",
            "description": "My project description",
            "tasks": [task.id for task in Task.query.all()],
            "users": [user.id for user in User.query.all()]
        }
