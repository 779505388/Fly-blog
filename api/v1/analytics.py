from flask_restplus import Namespace, Resource
from flask import jsonify
from models.Other import View
from tool import getAnalyTime
api = Namespace("analytics", description="访问统计")


@api.route("/")
class Analytics(Resource):
    def get(self):
        view = View.query.filter_by(created=getAnalyTime()).first()
        if view:  # 当日访问如果记录存在
            view.views += 1
            view.updata()
        else:
            view = View(views=1)
            view.save()
        return jsonify("访问+1")
