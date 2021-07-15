from extension import db
from datetime import datetime, timezone
from tool import getAnalyTime


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
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False

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
            return True
        except Exception as error:
            print(error)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def updata(self):
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
