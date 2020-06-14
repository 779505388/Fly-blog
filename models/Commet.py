from extension import db
from datetime import datetime
from tool import Md5
import uuid


class ParentComment(db.Model):
    __tablename__ = "parent_commet"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, index=True)
    created = db.Column(db.DateTime, default=datetime.now)
    guest_name = db.Column(db.String(200), nullable=False)
    guest_email = db.Column(db.String(300), nullable=False)
    hash_email = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    web_site = db.Column(db.String(300), nullable=True)
    uuid = db.Column(db.String(300), nullable=True)

    def __init__(self, *args, **kwargs):
        email = kwargs.get("guest_email")
        guest_name = kwargs.get("guest_name")
        post_id = kwargs.get("post_id")
        text = kwargs.get("text")
        web_site = kwargs.get("web_site")

        self.guest_email = email
        self.hash_email = Md5(email)
        self.guest_name = guest_name
        self.post_id = post_id
        self.text = text
        self.web_site = web_site
        self.uuid = str(uuid.uuid4())

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


class ChildrenCommet(db.Model):
    __tablename__ = "children_commet"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号id
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'parent_commet.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)  # 内容
    created = db.Column(db.DateTime, default=datetime.now)  # 发布时间
    guest_name = db.Column(db.Text, nullable=False)
    guest_email = db.Column(db.Text, nullable=False)
    hash_email = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    parent = db.relationship('ParentComment', backref=db.backref(
        'children_commets'), lazy='subquery')
    web_site = db.Column(db.String(300), nullable=True)
    uuid = db.Column(db.String(300), nullable=True)

    def __init__(self, *args, **kwargs):
        email = kwargs.get("guest_email")
        guest_name = kwargs.get("guest_name")
        post_id = kwargs.get("post_id")
        text = kwargs.get("text")
        web_site = kwargs.get("web_site")
        parent_id = kwargs.get("parent_id")

        self.guest_email = email
        self.hash_email = Md5(email)
        self.guest_name = guest_name
        self.post_id = post_id
        self.text = text
        self.web_site = web_site
        self.parent_id = parent_id
        self.uuid = str(uuid.uuid4())

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
