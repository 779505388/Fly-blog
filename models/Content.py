from extension import db
from datetime import datetime


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    slug = db.Column(db.String(400), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now)
    user_id = db.Column(db.Integer,  nullable=False)
    post_type = db.Column(db.String(100),  nullable=False)
    url_en = db.Column(db.String(200), unique=True, nullable=True)
    tag = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=True)
    template = db.Column(db.Text, nullable=True)
    like_count = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, nullable=True)
    __searchable__ = ["tag", "text", "title",
                      "slug", "url_en", "id"]

    def save(self):
        try:
            db.session.add(self)
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
