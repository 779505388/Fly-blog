from api.v1.auth import auth
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from models.Content import Article, Tag, Category
from extension import db

api = Namespace("category", description="文章分类数据接口")


@api.route("/")
class Type(Resource):
    """
    文章分类相关操作
    """

    def get(self):
        '''通过分类获取文章'''
        pageShow = 6
        category = request.args.get("category")
        page = request.args.get("page", type=int, default=1)
        categoryData = Category().query.filter(Category.name
                                               == category).first()
        total = categoryData.article.count()
        start = (page-1)*pageShow
        end = start + pageShow
        articles = categoryData.article.order_by(
            Article.created.desc()).slice(start, end)
        articleList = []
        for article in articles:
            data1 = article.to_json()
            data1.update(
                {"category": categoryData.name if categoryData else None})
            articleList.append(data1)
        return jsonify({
            "data": {"article": articleList,
                     "conuter": categoryData.article.count(),
                     'pageShow': pageShow}
        })


@api.route("/admin/")
class AdminCategory(Resource):
    '''管理文章分类接口'''
    @auth.login_required
    def get(self):
        categoryData = Category.query.all()
        category = []
        for n in categoryData:
            category.append(n.to_json())

        return jsonify({'data': {'category': category}})

    def post(self):
        category = api.payload['data'].get('category')
        blogCategory = Category(name=category)
        if blogCategory.save():
            categoryData = Category.query.all()
            category = []
            for n in categoryData:
                category.append(n.to_json())
            return jsonify({
                "code": 201,
                "status": "success",
                'message': '文章分类提交成功！',
                'data': {'category': category}
            })
        else:
            return jsonify({
                "code": 401,
                "status": "error",
                "message": '文章分类提交失败！'
            })

    def put(self):
        data = api.payload['data']
        id = data.get('id')
        category = Category.query.filter(Category.id == id).first_or_404()
        category.name = data.get('name')
        try:
            db.session.add(category)
            db.session.commit()
            return {
                "code": 201,
                "status": "success",
                'message': '文章分类修改成功！'
            }
        except Exception as eror:
            return {
                "code": 401,
                "status": "error",
                "message": eror
            }

    def delete(self):
        data = api.payload['data']
        id = data.get('id')
        category = Category.query.filter(Category.id == id).first_or_404()
        try:
            db.session.delete(category)
            db.session.commit()
            categoryData = Category.query.all()
            category = []
            for n in categoryData:
                category.append(n.to_json())
            return jsonify({
                "code": 201,
                "status": "success",
                'message': '文章分类修改成功！',
                'data': {'category': category}
            })
        except Exception as eror:
            return jsonify({
                "code": 401,
                "status": "error",
                "message": eror
            })
