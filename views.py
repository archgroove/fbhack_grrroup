from flask_restful import Resource, reqparse
import requests

__all__ = ["UserList", "TaskList", "Project", "GetTask", "GetUser", "ChangeTask", "ChangeUser", "CreateTask", "CreateUser", "GetUnassigned"]

class UserList(Resource):
    def get(self):
        from models import User, Task, TASK_STATUSES
        all_users = []
        for user in User.query.all():
            all_users.append(
                { 
                    "id": user.id,
                    "name": user.name,
                    "assigned_tasks": [task.id for task in user.tasks],
                    "photo_url": user.avatar if user.avatar else "photo_url.jpg"
                }
            )
        return all_users


class TaskList(Resource):
    def get(self):
        from models import User, Task, TASK_STATUSES
        all_tasks = []
        for task in Task.query.all():
            all_tasks.append({
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "assignee": task.assignee.id,
                "status": task.status,
                "color": "0000ff"
            })
        return all_tasks

class Project(Resource):
    def get(self):
        from models import User, Task, TASK_STATUSES
        project = {
            "name": "My project name",
            "description": "My project description",
            "tasks": [task.id for task in Task.query.all()],
            "users": [user.id for user in User.query.all()]
        }
        return project


class GetTask(Resource):
    def get(self, task_id):
        from models import User, Task, TASK_STATUSES
        task = Task.query.get(int(task_id))
        if task is None:
            return None
        ret_task = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "assignee": task.assignee.id,
            "status": task.status,
            "color": "0000ff"
        }
        return ret_task


class GetUser(Resource):
    def get(self, user_id):
        from models import User, Task, TASK_STATUSES
        user = User.query.get(int(user_id))
        if user is None: 
            return None
        ret_user = {
            "name": user.name,
            "assigned_tasks": [task.id for task in user.tasks],
            "photo_url": "static_photo.jpg"
        }
        return ret_user


class ChangeTask(Resource):
    def put(self, task_id):
        
        from models import User, Task, TASK_STATUSES
        from app import db
        
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('assigned_id', type=int)
        parser.add_argument('status', type=str)
        parser.add_argument('color', type=str)
        args = parser.parse_args()

        if 'message' in args: # we think message indicates an error
            return {"status": False, "message": parser['message']}
        
        if args.status is not None and not args.status in TASK_STATUSES:
            return {"status": False, "message": "Invalid task status"}

        # Fail if assigned id was supplied but is invalid
        if not args.assigned_id is None and User.query.get(args.assigned_id) is None:
            return {"status": False, "message": "Invalid assigned id"}

        t = Task.query.get(task_id)
        if args.name:
            t.name = args.name
        if args.description:
            t.description = args.description
        if args.assigned_id:
            t.assigned_id = args.assigned_id
        if args.status:
            t.status = args.status
        if args.color:
            t.color = args.color
        db.session.add(t)
        db.session.commit()

        return {
            'status': True,
            'task': {
                "name": t.name,
                "description": t.description,
                "assignee": t.assigned_id,
                "status": t.status,
                "color": t.color
            }
        }


class ChangeUser(Resource):
    def put(self, user_id):
        
        from models import User
        from app import db

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('facebook_details', type=str)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('avatar', type=str, required=False) # a filepath
        args = parser.parse_args()

        u = User.query.get(user_id)
       
        if 'message' in args:
            return {"status": False, "message": args['message']}

        if u is None:
            return {"status": False, "message": "No such user"}

        u = User()
        if args.facebook_details:
            u.facebook_details = args.facebook_details
        if args.name:
            u.name = args.name
        if args.email:
            u.email = args.email
        if args.avatar:
            u.avatar = args.avatar
        db.session.add(u)
        db.session.commit()

        return {
            "status": True,
            "user": {
                "facebook_details": u.facebook_details,
                "name": u.name,
                "email": u.email,
                "avatar": u.avatar
            }
        }
         


class CreateTask(Resource):
    def post(self):
        from models import User, Task, TASK_STATUSES
        from app import db
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, default="")
        parser.add_argument('assigned_id', type=int)
        parser.add_argument('status', type=str, required=True)
        parser.add_argument('color', type=str, default="0000ff")
        args = parser.parse_args()

        if not args.status in TASK_STATUSES:
            return {"status": False, "message": "Invalid task status"}

        if 'message' in args: # we think message indicates an error
            return {"status": False, "message": parser['message']}

        # Fail if assigned id was supplied but is invalid
        if not args.assigned_id is None and User.query.get(args.assigned_id) is None:
            return {"status": False, "message": "Invalid assigned id"}

        t = Task()
        t.name = args.name
        t.description = args.description
        t.assignee = None if not args.assigned_id else args.assigned_id
        
        t.status = args.status
        t.color = args.color
        db.session.add(t)
        db.session.commit()

        return {
            'status': True,
            'task': {
                "name": args.name,
                "description": args.description,
                "assignee": None if not args.assigned_id else args.assigned_id,
                "status": args.status,
                "color": args.color
            }
        }


class CreateUser(Resource):
    def post(self):
        from models import User, Task, TASK_STATUSES
        from app import db
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('facebook_details', type=str)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('avatar', type=str, required=False)
        args = parser.parse_args()

        u = User()
        u.facebook_details = args.facebook_details
        u.name = args.name
        u.email = args.email
        u.avatar = args.avatar
        db.session.add(u)
        db.session.commit()

        return {
            "status": True,
            "user": {
                "facebook_details": args.facebook_details,
                "name": args.name,
                "email": args.email,
                "avatar": args.avatar
            }
        }

#class UpdateAvatar(Resource):
#    def post(self, user_id):
#        parser=reqparse.RequestParser(bundle_errors=True)
#        parser.add_argument('avatar', type=str) # a filepath
#        args = parser.parser_args()
#
#        if 'message' in args:
#            return {"status": False, "message": "Incorrect avatar"}
#    
#        u = User.query.get(user_id)
#        if args.avatar:
#            u.avatar = args.avatar
#        db.session.add(u)
#        db.session.commit()
#        
#        return {
#            "status": True,
#            "user": {
#                "id": u.id,
#                "avatar": u.avatar
#            }
#        }

class GetUnassigned(Resource):
    def get(self):
        from models import Task

        unassigned_tasks = []
        for task in Task.query.filter(Task.assignee==None):
            unassigned_tasks.append({
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "assignee": task.assignee.id,
                "status": task.status,
                "color": "0000ff"
            })
        return unassigned_tasks

        

