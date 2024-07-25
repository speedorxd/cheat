from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return "working 😁"

api.add_resource(Greeting, '/')

host = "0.0.0.0"
port = 8080  

app.run(host=host, port=port)
