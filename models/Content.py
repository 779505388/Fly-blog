from extension import db
from datetime import datetime


article_tag = db.Table('article_tag',
                       db.Column('article_id', db.Integer, db.ForeignKey(
                           'article.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey(
                           'tag.id'), primary_key=True)
                       )

article_category = db.Table('article_category',
                            db.Column('article_id', db.Integer, db.ForeignKey(
                                'article.id'), primary_key=True),
                            db.Column('category_id', db.Integer, db.ForeignKey(
                                'category.id'), primary_key=True)
                            )


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    slug = db.Column(db.String(400), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now,
                         onupdate=datetime.now)
    user_id = db.Column(db.Integer,  nullable=False)
    url_en = db.Column(db.String(200), unique=True, nullable=False)
    image_url = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=False)
    template = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, nullable=True)
    __searchable__ = ["text", "title",
                      "slug", "url_en", "id"]
    tags = db.relationship('Tag', secondary=article_tag,
                           backref=db.backref('articles', lazy="dynamic"),
                           lazy="dynamic")
    category = db.relationship('Category', secondary=article_category,
                               backref=db.backref('articles', lazy="dynamic"),
                               lazy="dynamic")

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

    def paginate(self):
        print(self)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

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


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

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
