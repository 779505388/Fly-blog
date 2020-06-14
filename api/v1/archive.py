from flask_restplus import Namespace, Resource
from flask import jsonify, request
from api.v1.auth import auth
from models.Content import Content

api = Namespace("archive", description="归档数据接口")


@api.route("/")
class Archive(Resource):
    def get(self):
        content_start = Content.query.first()
        startTime = content_start.created
        content_end = Content.query.order_by(Content.created.desc()).first()
        endTime = content_end.created
        return jsonify({"startTime": str(startTime), "endTime": str(endTime)})

    def post(self):
        data = request.get_json()
        contents = Content.query.filter(
            Content.created >= data["start"]).filter(
            Content.created < data["end"]).all()
        data_list = []
        for data1 in contents:
            data_list.append(data1.to_json())
        return jsonify(data_list)

    def delete(self):
        print(api.payload)
        return "ok"
