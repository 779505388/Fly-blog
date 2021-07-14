from extension import db
from datetime import datetime, timezone
import hashlib
import uuid


def Md5(email):
    md = hashlib.md5()  # 构造一个md5
    md.update(email.encode())
    return md.hexdigest()


def utcTime():
    '''返回utc时间'''
    return datetime.utcnow


class Comment(db.Model):
    __tablename__ = "commet"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, nullable=True, index=True)
    parent_id = db.Column(db.Integer, nullable=True)
    parent_uuid = db.Column(db.String(500), nullable=True, index=True)
    parent_name = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, nullable=True, index=True)
    agent = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    comment_type = db.Column(db.String(300), nullable=False)
    guest_name = db.Column(db.String(200), nullable=False)
    guest_email = db.Column(db.String(300), nullable=False)
    hash_email = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    web_site = db.Column(db.String(300), nullable=True)
    uuid = db.Column(db.String(300), nullable=True)
    show_status = db.Column(db.Boolean, default=False)  # 默认评论不可见

    def __init__(self, *args, **kwargs):
        email = kwargs.get("guest_email")
        guest_name = kwargs.get("guest_name")
        post_id = kwargs.get("post_id")
        text = kwargs.get("text")
        web_site = kwargs.get("web_site")
        show_status = kwargs.get("show_status")
        parent_id = kwargs.get('parent_id')
        user_id = kwargs.get("user_id")
        agent = kwargs.get("agent")
        comment_type = kwargs.get('comment_type')
        self.parent_name = kwargs.get('parent_name')
        self.parent_uuid = kwargs.get('parent_uuid')
        self.user_id = user_id
        self.parent_id = parent_id
        self.show_status = show_status
        self.comment_type = comment_type
        self.agent = agent
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
