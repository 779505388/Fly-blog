from flask_restplus import Namespace, Resource, marshal, fields, marshal_with
from flask import jsonify, request
from models.Content import Article

api = Namespace("index", description="首页数据接口")


@api.route("/")
class Index(Resource):

    def get(self):
        page = request.args.get("page", type=int, default=1)
        page_content = 6
        total = Article.query.count()
        start = (page-1)*page_content
        end = start + page_content
        contents = Article.query.order_by(
            Article.created.desc()).slice(start, end)
        data = []
        for content in contents:
            category = content.category.first()
            data1 = content.to_json()
            del data1["template"]
            del data1["text"]
            data1.update({'category':category.name if category else None})
            data.append(data1)
        return jsonify({
            "data": {"article": data, "conuter": total, 'pageShow': 6}
        })
