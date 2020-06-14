from flask_restplus import Namespace, Resource
from flask import jsonify
from models.User import User
from api.v1.auth import auth, serializer

api = Namespace("token", description="JWT 接口")


@api.route("/")
class Login(Resource):
    def get(self):
        return jsonify(
            {
                "code": 201,
                "message": "Token Port"
            }
        )

    def post(self):
        data = api.payload["login"]
        username = data['username']
        password = data["password"]

        user = User.query.filter_by(
            username=username).first_or_404()

        if user.check_password(password):
            print(user.username)
            token = serializer.dumps({"username": username})
            return jsonify({"token": token.decode()})
        else:
            return jsonify("Email Or Password Error")
        return jsonify(api.payload)

    def delete(self):
        return {"code": 200, "message": "success"}
