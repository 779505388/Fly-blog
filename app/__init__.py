from flask import Flask
from views.article.article import article
from views.admin.admin import admin
from extension import config_init
from api.api_v1 import api_v1
from api.api_v2 import api_v2
from logging.handlers import TimedRotatingFileHandler
import logging
from tool import getCategory, getItem, getInfo

def create_app(config):
    app = Flask(__name__, template_folder='./templates/',
                static_folder='./static/')
    app.register_blueprint(article)
    app.register_blueprint(admin)
    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)
    app.config.from_object(config)

    # 全局变量，获取文章分类
    app.add_template_global(getCategory, 'getCategory')
    app.add_template_global(getItem, 'getItem')
    app.add_template_global(getInfo, 'getInfo')
    config_init(app)

    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "FlyBlog.log", when="D", interval=15, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    return app
