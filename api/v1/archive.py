from flask_restplus import Namespace, Resource
from flask import jsonify, request
from api.v1.auth import auth
from models.Content import Article
import time
api = Namespace("archive", description="归档数据接口")


@api.route("/")
class Archive(Resource):
    def get(self):
        content_start = Article.query.first()
        startTime = content_start.created
        content_end = Article.query.order_by(Article.created.desc()).first()
        endTime = content_end.created
        return jsonify({'data': {"startTime": str(startTime), "endTime": str(endTime)}})

    def post(self):
        data = request.get_json()
        page = int(data.get('page'))
        print(data)
        page_content = 6
        start = (page-1)*page_content
        end = start + page_content
        counter = contents = Article.query.filter(
            Article.created >= time.strptime(data["start"]+'-1', "%Y-%m-%d")).filter(
            Article.created < time.strptime(data["end"]+'-1', "%Y-%m-%d")).count()
        print(data)
        contents = Article.query.filter(
            Article.created >= time.strptime(data["start"]+'-1', "%Y-%m-%d")).filter(
            Article.created < time.strptime(data["end"]+'-1', "%Y-%m-%d")).order_by(
            Article.created.desc()).slice(start, end)
        data_list = []
        for content in contents:
            category = content.category.first()
            articleData = content.to_json()
            articleData.update(
                {'category': category.name if category else None})
            data_list.append(articleData)
        return jsonify({'data': {'article': data_list,
                                 'pageShow': page_content, 'conuter': counter}})

    def delete(self):
        print(api.payload)
        return "ok"
