from flask import Flask
from views.article.article import article
from views.admin.admin import admin
from extension import config_init
from api.api_v1 import api_v1
from api.api_v2 import api_v2


def create_app(config):
    app = Flask(__name__, template_folder='./templates/',
                static_folder='./static/')
    app.register_blueprint(article)
    app.register_blueprint(admin)
    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)
    app.config.from_object(config)
    config_init(app)

    return app
