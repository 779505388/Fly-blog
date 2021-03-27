from flask_restplus import Namespace, Resource, marshal, fields, marshal_with
from flask import jsonify, request
from models.Content import Article

api = Namespace("search", description="搜索数据接口")


@api.route("/")
class Search(Resource):

    def get(self):
        page = request.args.get("page", type=int, default=1)
        search = request.args.get("search")
        page_content = 6
        total = Article.query.msearch(search).count()
        start = (page-1)*page_content
        end = start + page_content
        contents = Article.query.msearch(search).order_by(
            Article.created.desc()).slice(start, end)
        data = []
        print(contents)
        for content in contents:
            data1 = content.to_json()
            del data1["template"]
            del data1["text"]
            data.append(data1)
        return jsonify({
            "data": {"article": data, "conuter": total, 'pageShow': 6}
        })
