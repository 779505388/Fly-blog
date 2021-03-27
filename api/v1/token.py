from flask_restplus import Namespace, Resource
from flask import jsonify, request
from models.User import User
from api.v1.auth import auth, serializer
from models.Content import Article, Tag, Category
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
        # 获取token
        data = api.payload["login"]
        username = data['username']
        password = data["password"]

        user = User.query.filter_by(
            username=username).first()
        print(user)
        if user:
            if user.check_password(password):
                print(user.username)
                token = serializer.dumps({"username": username})
                return jsonify({"token": token.decode(), 'status': 'success', 'message': '登陆成功！'})
            else:
                return jsonify({'status': 'error', 'message': '用户名或密码错误！'})
            return jsonify(api.payload)
        else:
            return jsonify({'status': 'error', 'message': '用户不存在！'})

    def put(self):
        # 验证登陆状态
        headers = request.headers.get('Authorization').split(' ')
        token = headers[1]
        categoryData = Category.query.all()
        category = []
        for n in categoryData:
            category.append(n.to_json().get('name'))
        try:
            data = serializer.loads(token)
        except Exception as e:

            return {"code": 401,
                    "message": "error",
                    'login': False,
                    'data': {'category': category}}
        if 'username' in data:
            return {"code": 200,
                    "message": "success",
                    'login': True,
                    'data': {'category': category}}

        return {"code": 401, "error": "error", 'login': False}
