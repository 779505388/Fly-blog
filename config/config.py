import os
from config.rw_json import read_json


class Base():
    DEBUG = True


class DevConfig():
    DEBUG = True
    JSON_AS_ASCII = False
    RESTFUL_JSON = dict(ensure_ascii=False)
    INFO = read_json()
    USERNAME = "Your Name"
    PASSWORD = "Your Password"
    HOST = "127.0.0.1"
    PORT = "3306"
    DB = "DataBase Name"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOST, PORT, DB
    )
    BLOGNAME = INFO["blogConfig"]["blogName"]
    SECRET_KEY = "sadad232@42134@!>?"
    WTF_CSRF_SECRET_KEY = os.urandom(24)
    SCHEDULER_API_ENABLED = True
    WHOOSH_ENABLE = True
    MSEARCH_BACKEND = 'whoosh'
    MSEARCH_INDEX_NAME = 'msearch'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MSEARCH_INDEX_NAME = 'whoosh_index'
    WHOOSH_BASE = 'whoosh_index'
    MSEARCH_ENABLE = True
    
