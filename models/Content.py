from extension import db
from datetime import datetime
from jieba.analyse import ChineseAnalyzer
from flask import current_app

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
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer,  nullable=False)
    url_en = db.Column(db.String(200), unique=True, nullable=False)
    image_url = db.Column(db.String(100), nullable=True)
    text = db.Column(db.Text, nullable=False)
    template = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, nullable=True)
    __searchable__ = ["text", "title",
                      "slug", "url_en"]
    __msearch_analyzer__ = ChineseAnalyzer()
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
            current_app.logger.info('文章保存成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章保存错误{}：'.format(error))
            return {'status': False, "message": error}

    def updata(self):
        try:
            db.session.commit()
            current_app.logger.info('文章更新成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章保存错误{}：'.format(error))
            return {'status': False, "message": error}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('文章删除成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章删除错误{}：'.format(error))
            return {'status': False, "message": error}

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
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('标签保存成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('标签保存错误{}'.format(error))
            return {'status': False, "message": error}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('标签删除成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('标签删除错误{}'.format(error))
            return {'status': False, "message": error}

    def updata(self):
        try:
            db.session.commit()
            current_app.logger.info('标签更新成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('标签更新错误{}'.format(error))
            return {'status': False, "message": error}

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('文章分类保存成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章分类保存错误{}'.format(error))
            return {'status': False, "message": error}

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('文章分类删除成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章分类删除错误{}'.format(error))
            return {'status': False, "message": error}

    def updata(self):
        try:
            db.session.commit()
            current_app.logger.info('文章分类更新成功')
            return {'status': True}
        except Exception as error:
            current_app.logger.error('文章分类更新错误{}'.format(error))
            return {'status': False, "message": error}

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
