from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_caching import Cache
from flask_apscheduler import APScheduler
from flask_msearch import Search
from jieba.analyse import ChineseAnalyzer

db = SQLAlchemy()
bcrypt = Bcrypt()
moment = Moment()
cache = Cache()
scheduler = APScheduler()
search = Search(analyzer=ChineseAnalyzer())


def config_init(app):
    db.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    cache.init_app(app)
    search.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
