from flask_restplus import Namespace, Resource
from flask import jsonify
from models.User import User

api = Namespace("register", description="注册")


@api.route("/")
class Register(Resource):
    def get(self):
        return jsonify("注册端口")

    def post(self):
        data = api.payload

        if data["token"] == "123456789":
            logon_data = data["register"]
            mail = logon_data["mail"]
            username = logon_data["username"]
            password = logon_data["password"]
            user = User(username=username, mail=mail, password=password)
            if user.save_on():
                return jsonify("register is ok")
            else:
                return jsonify("error")

        return jsonify(data)
