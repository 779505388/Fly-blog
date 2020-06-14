from flask_restplus import Namespace, Resource, marshal, fields, marshal_with
from flask import jsonify, request
from models.Content import Content

api = Namespace("index", description="首页数据接口")


@api.route("/")
class Index(Resource):

    def get(self):
        page = request.args.get("page", type=int, default=1)
        page_content = 6
        total = Content.query.count()
        start = (page-1)*page_content
        end = start + page_content
        contents = Content.query.order_by(
            Content.created.desc()).slice(start, end)
        data = []
        for content in contents:
            data.append(content.to_json())
        return jsonify({
            "data": {"article": data, "conuter": total}
        })
