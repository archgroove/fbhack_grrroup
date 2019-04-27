from flask_restful import Resource
from models import User


class UserList(Resource):
    def get(self):
        all_users = []
        for user in User.query.all():
            all_users.append(
                { 
                    'name': user.name,
                }
            )
        return all_users
