from flask import Blueprint
from flask_restplus import Api
from api.v1.index import api as index
from api.v1.article import api as article
from api.v1.register import api as register
from api.v1.token import api as token
from api.v1.archive import api as archive
from api.v1.captcha import api as captcha
from api.v1.tags import api as tags
#from api.v1.comment import api as comment
from api.v1.search import api as search
from api.v1.category import api as category
from extension import csrf

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(api_v1, version="1.0")

api.add_namespace(index)
api.add_namespace(article)
api.add_namespace(register)
api.add_namespace(token)
api.add_namespace(archive)
api.add_namespace(captcha)
api.add_namespace(tags)
#api.add_namespace(comment)
api.add_namespace(search)
api.add_namespace(category)
csrf.exempt(api_v1)