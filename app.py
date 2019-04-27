from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/tfpk/code/hack/test.db'
db = SQLAlchemy(app)

api.add_resource(Users, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)

