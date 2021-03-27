from flask_restplus import Namespace, Resource, marshal, fields, marshal_with
from flask import jsonify, request
from models.Content import Article, Tag
from api.v1.auth import auth
api = Namespace("tags", description="标签")


@api.route("/")
class Tags(Resource):

    def get(self):

        tags = Tag().query.all()
        data = []
        for tag in tags:
            data.append(tag.name)
        return jsonify({
            "data": {"tags": data}
        })

    def post(self):
        postData = api.payload

        tags = Tag.query.filter(Tag.name == postData.get('tag')).first()
        contents = tags.articles
        data = []
        for content in contents:
            category = content.category.first()
            data1 = content.to_json()
            del data1["template"]
            del data1["text"]
            data1.update({'category':category.name if category else None})
            data.append(data1)
        total = len(data)
        page = postData.get('tagPage')
        page_content = 6
        start = (page-1)*page_content
        end = start + page_content-1
        return jsonify({
            "data": {"article": data[start:end],
                     "conuter": total, 'pageShow': page_content}
        })


@api.route("/admin/")
class AdminTag(Resource):
    @auth.login_required
    def get(self):
        tags = Tag.query.all()
        tagData = []
        for i in tags:
            tagData.append(i.name)
        return jsonify({
            "data": {"tags": tagData}
        })

    @auth.login_required
    def post(self):
        return 'ok'

    @auth.login_required
    def delete(self):
        data = api.payload['data']
        tag = Tag.query.filter(Tag.name == data.get('tag')).first()
        if tag.delete():
            tags = Tag.query.all()
            tagData = []
            for i in tags:
                tagData.append(i.name)
            return jsonify({
                "data": {"tags": tagData},
                "code": 200,
                "status": "success",
                'message': '删除标签成功！'
            })
        else:
            return {
                "code": 401,
                "status": "error",
                "message": '提交到了服务器，但是出现了错误！'
            }
