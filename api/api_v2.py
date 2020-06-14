from flask import Blueprint
from flask_restplus import Api, Resource


api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")
api = Api(api_v2, version="2.0")


@api.route("/home")
class Home(Resource):
    def get(self):
        return {"aa": "AA"}
