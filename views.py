from flask_restful import Resource
from models import User


class Users(Resource):
    def get(self):
        return User.query.all()
