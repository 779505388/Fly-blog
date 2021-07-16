from flask.globals import current_app
from extension import db
from datetime import datetime, timezone
from tool import getAnalyTime
from flask import current_app


class PyLink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    avatar = db.Column(db.String(1000), nullable=False)
    brief = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('友链保存成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('友链保存错误{}：'.format(error))
            return {'status': False, "message": error}

    def updata(self):
        try:
            db.session.commit()
            current_app.logger.info('友链更新成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('友链更新错误{}：'.format(error))
            return {'status': False, "message": error}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('友链删除成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('友链删除错误{}：'.format(error))
            return {'status': False, "message": error}

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class View(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    views = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=getAnalyTime())

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('访问记录保存成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('访问记录保存错误{}：'.format(error))
            return {'status': False, "message": error}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('访问记录删除成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('访问记录删除错误{}：'.format(error))
            return {'status': False, "message": error}

    def updata(self):
        try:
            db.session.commit()
            current_app.logger.info('访问记录更新成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('访问记录更新错误{}：'.format(error))
            return {'status': False, "message": error}

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
