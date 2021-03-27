from api.v1.auth import auth
from flask import jsonify, request
from flask_restplus import Namespace, Resource
from models.Content import Article, Tag, Category
from extension import db


api = Namespace("article", description="文章数据接口")


@api.route("/")
class Post(Resource):
    def get(self):
        id = request.args.get("id")

        content = Article.query.filter(Article.url_en == id).first_or_404()
        # content = Article.query.filter(Article.id == 10).first_or_404()
        contents = Article.query.all()
        paginate = []
        for n in contents:
            paginate.append(n.id)
        print(paginate.index(content.id), paginate)
        if len(paginate) <= 1:
            nextPage = ''
            prePage = ''
        elif paginate[0] == content.id:
            nextArticle = Article.query.filter(
                Article.id == paginate[1]).first_or_404()
            nextPage = {'page': True, 'route': nextArticle.url_en}
            prePage = ''
        elif paginate[len(paginate)-1] == content.id:
            nextPage = ''
            preArticle = Article.query.filter(
                Article.id == paginate[-2]).first_or_404()
            prePage = {'page': True, 'route': preArticle.url_en}
        else:
            nextIndex = paginate.index(content.id)+1
            nextArticle = Article.query.filter(
                Article.id == paginate[nextIndex]).first_or_404()
            nextPage = {'page': True, 'route': nextArticle.url_en}

            preIndex = paginate.index(content.id) - 1
            preArticle = Article.query.filter(
                Article.id == paginate[preIndex]).first_or_404()
            prePage = {'page': True, 'route': preArticle.url_en}
        print(content.tags)
        tagsData = []
        for tag in content.tags:
            tagsData.append(tag.name)
        articleData = content.to_json()
        articleData.update({'tags': tagsData})
        return jsonify({"data": {
            "article": articleData, 'articleId': content.id,
            'nextPage': nextPage, 'prePage': prePage
        }})


@api.route("/admin/")
class AdminPost(Resource):
    # 得到全部文章 or 单独文章
    @auth.login_required
    def get(self):
        id = request.args.get("id")
        if id:
            content = Article.query.filter(
                Article.id == int(id)).first_or_404()
            tagsList = []
            for i in content.tags:
                tagsList.append(i.name)
            category = content.category.first()
            articleData = content.to_json()
            articleData.update({'tags': tagsList,
                                'category': category.name if category else ''})
            return jsonify({
                "data": {"article": articleData}
            })
        contents = Article.query.all()
        data = []
        for content in contents:
            data1 = content.to_json()
            del data1["template"]
            del data1["text"]
            data.append(data1)
        return jsonify({
            "data": {"article": data}
        })

    @auth.login_required
    # 提交新文章
    def post(self):
        data = api.payload["data"]["article"]
        title = data.get("title")
        slug = data.get("slug")
        user_id = data.get("user_id")
        post_type = data.get("post_type")
        url_en = data.get("url_en")
        tag = data.get("tag")
        image_url = data.get("image_url")
        text = data.get("text")
        template = data.get("template")
        like_count = data.get("like_count")
        views = data.get("views")

        content = Article(title=title, slug=slug, user_id=user_id,
                          url_en=url_en,
                          image_url=image_url,
                          text=text, template=template, like_count=like_count,
                          views=views,
                          )
        tagList = data.get("tag")
        for i in tagList:
            blogTag = Tag().query.filter(Tag.name == i).first()
            if blogTag:
                content.tags.append(blogTag)
                db.session.add(blogTag)
                print(blogTag)
            else:
                blogTag = Tag(name=i)
                content.tags.append(blogTag)
                db.session.add(blogTag)
        '''文章分类'''
        blogCategory = Category().query.filter(Tag.name == post_type).first()
        if blogCategory:
            content.category.append(blogCategory)
            db.session.add(blogCategory)
        else:
            blogCategory = Category(name=post_type)
            content.category.append(blogCategory)
            db.session.add(blogCategory)
        db.session.add(content)
        db.session.commit()
        return {
            "code": 200,
            "status": "success",
            'message': '文章提交成功！'
        }

    @auth.login_required
    # 修改文章
    def put(self):
        data = api.payload["data"]["article"]
        id = api.payload["data"].get('id')

        content = Article.query.filter(Article.id == id).first_or_404()
        tagRemove = content.tags.all()
        print(tagRemove, 'bbbb')
        if len(tagRemove) != 0:
            for n in tagRemove:
                print(n.name, 'aa')
                content.tags.remove(n)
        content.title = data.get("title")
        content.slug = data.get("slug")
        content.user_id = data.get("user_id")
        category = data.get("category")
        content.url_en = data.get("url_en")
        tags = data.get("tags")
        content.image_url = data.get("image_url")
        content.text = data.get("text")
        content.template = data.get("template")
        content.like_count = data.get("like_count")
        content.views = data.get("views")
        for i in tags:
            blogTag = Tag().query.filter(Tag.name == i).first()
            if blogTag:
                content.tags.append(blogTag)
                db.session.add(blogTag)
            else:
                blogTag = Tag(name=i)
                content.tags.append(blogTag)
                db.session.add(blogTag)
        delCategory = content.category.first() if content.category.first() else False
        if delCategory:
            content.category.remove(delCategory)
        blogCategory = Category().query.filter(Category.name ==
                                               category).first()
        if blogCategory:
            content.category.append(blogCategory)
            db.session.add(blogCategory)
        else:
            blogCategory = Category(name=category)
            content.category.append(blogCategory)
            db.session.add(blogCategory)

        try:
            content.save()
            return {
                "code": 201,
                "status": "success",
                'message': '文章修改成功！'
            }
        except Exception as eror:
            print(eror)
            return {
                "code": 401,
                "status": "error",
                "message": eror
            }

    @auth.login_required
    def delete(self):
        articleId = api.payload['data'].get('articleId')
        error = 0
        success = 0
        for id in articleId:
            content = Article.query.filter(Article.id == int(id)).first()

            if content.delete():
                success += 1

            else:
                error += 1
        print(api.payload)
        contents = Article.query.all()
        data = []
        for content in contents:
            data1 = content.to_json()
            del data1["template"]
            del data1["text"]
            data.append(data1)
        return jsonify({
            "code": 200,
            "status": "success",
            'message': '删除成功{}，删除失败{}'.format(success, error),
            "data": {"article": data}
        })
