import os
from config.rw_json import read_json


class Base():
    DEBUG = True


class DevConfig():
    DEBUG = True
    JSON_AS_ASCII = False
    RESTFUL_JSON = dict(ensure_ascii=False)
    INFO = read_json()
    USER_EMAIL_HASH = ''
    USERNAME = ""  # your name
    PASSWORD = ""  # your passwo
    HOST = "127.0.0.1"
    PORT = "3306"
    DB = "flask"  # 数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOST, PORT, DB
    )
    BLOGNAME = INFO["blogConfig"]["blogName"]
    SECRET_KEY = "teryhedhhr"  # 一定要修改！！
    WTF_CSRF_SECRET_KEY = os.urandom(24)
    SCHEDULER_API_ENABLED = True
    WHOOSH_ENABLE = True
    MSEARCH_BACKEND = 'whoosh'
    MSEARCH_INDEX_NAME = 'msearch'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MSEARCH_INDEX_NAME = 'whoosh_index'
    WHOOSH_BASE = 'whoosh_index'
    MSEARCH_ENABLE = True
    TEMPLATES_AUTO_RELOAD = True  # 刷新模板

    # flask-caching setting
    CACHE_TYPE = 'SimpleCache'  # RedisCache
    CACHE_REDIS_HOST = '127.0.0.1',
    CACHE_REDIS_PORT = 6379
    CACHE_KEY_PREFIX = 'FlyBlog'
