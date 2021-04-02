from flask import url_for, render_template, Blueprint, request, session,\
    redirect, jsonify, current_app
from flask_wtf.csrf import generate_csrf
from models.Content import Article, Tag, Category
from models.Commet import Comment
from models.Other import PyLink
from tool import get_server_info, login_required, sys_name
from extension import db

admin = Blueprint("admin", __name__,
                  template_folder="../../views/admin/templates/",
                  static_folder="../../views/admin/static/",
                  static_url_path="/admin/"
                  )


@admin.route("/admin/blog-info/", methods=['GET', "POST"])
@login_required
def blog_info():
    if request.method == 'GET':
        return render_template("blog-info.html")
    else:
        data = get_server_info()
        return jsonify(data)
# 博客信息


@admin.route("/admin/blog-write/", methods=["POST", "GET"])
@login_required
def blog_write():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        slug = data.get('slug')
        tags = data.get('tags')
        post_type = data.get('category')
        text = data.get('text')
        url_en = data.get("enUrl")
        user_id = 2
        image_url = data.get("img")
        template = data.get("template")
        article = Article(title=title, slug=slug, user_id=user_id, url_en=url_en,
                          image_url=image_url,
                          text=text, template=template
                          )
        print(tags)
        for i in tags:
            blogTag = Tag().query.filter(Tag.name == i).first()
            if blogTag:
                article.tags.append(blogTag)
                db.session.add(blogTag)
                print(blogTag)
            else:
                blogTag = Tag(name=i)
                article.tags.append(blogTag)
                db.session.add(blogTag)
        blogCategory = Category().query.filter(Category.name == post_type).first()
        if blogCategory:
            article.category.append(blogCategory)
            db.session.add(blogCategory)
        else:
            blogCategory = Category(name=post_type)
            article.category.append(blogCategory)
            db.session.add(blogCategory)
        db.session.add(article)
        db.session.commit()
        # if content.save():
        current_app.logger.info("发布文章成功")
        return jsonify({'status': "success"})
    else:
        return render_template("blog-write.html", **locals())

# 创建新文章


@admin.route("/admin/blog-list/", methods=["GET", "POST", "DELETE"])
@login_required
def blog_list():
    if request.method == "GET":
        return render_template("blog-list.html")
    elif request.method == "POST":
        content_list = Article.query.all()
        data_list = []
        for data in content_list:
            data_list.append(data.to_json())
        return jsonify(data_list)
    elif request.method == 'DELETE':
        data = request.get_json()
        print(data)
        if len(data["article"]) != 0:
            for article_id in data["article"]:

                content = Article.query.filter(
                    Article.id == article_id.get('id')).first()
                print('eeeeeee', content)
                if content.delete():
                    content_list = Article.query.all()
                    data_list = []
                    for data in content_list:
                        data_list.append(data.to_json())
                    current_app.logger.info("文章删除成功")
                    return jsonify({'status': "success",
                                    "message": ' 删除成功！', 'data': data_list})
                else:
                    return jsonify({'status': "error", "message": ' 删除错误！'})

        return jsonify({"ok": "ok"})
# 文章列表


@admin.route("/admin/blog-modify/<int:url>", methods=["GET", "POST", "PUT"])
@login_required
def blog_modify(url):
    if request.method == "GET":
        url = url
        return render_template("blog-modify.html", **locals())
    elif request.method == 'PUT':
        data = request.get_json()
        title = data.get('title')
        slug = data.get('slug')
        tags = data.get('tags')
        post_type = data.get('category')
        text = data.get('text')
        url_en = data.get("enUrl")
        image_url = data.get("img")
        template = data.get("template")
        print(data)
        content = Article.query.filter_by(id=url).first()
        for tag in content.tags:
            content.tags.remove(tag)
        for category in content.category:
            content.category.remove(category)
        for i in tags:
            blogTag = Tag().query.filter(Tag.name == i).first()
            if blogTag:
                content.tags.append(blogTag)
                db.session.add(blogTag)
                print(blogTag)
            else:
                blogTag = Tag(name=i)
                content.tags.append(blogTag)
                db.session.add(blogTag)
        blogCategory = Category().query.filter(Category.name == post_type).first()
        if blogCategory:
            content.category.append(blogCategory)
            db.session.add(blogCategory)
        else:
            blogCategory = Category(name=post_type)
            content.category.append(blogCategory)
            db.session.add(blogCategory)
        content.title = title
        content.slug = slug
        # content.post_type = post_type
        content.text = text
        content.url_en = url_en
        # content.tags = tags
        content.image_url = image_url
        content.template = template
        if content.updata():
            current_app.logger.info("文章修改成功")
            return jsonify({'status': "success",
                            "message": ' 修改成功！'})

        else:
            current_app.logger.info("文章修改失败")
            return "错误", 302

    elif request.method == "POST":
        content = Article.query.filter(
            Article.id == url).first()
        tags = []

        for tag in content.tags:
            tags.append(tag.name)
        category = content.category[0].name
        articleData = content.to_json()
        articleData['tags'] = tags
        articleData['category'] = category
        return jsonify(articleData)
# 修改文章


@admin.route("/admin/blog-delete/", methods=["GET", "POST"])
@login_required
def blog_delete():
    if request.method == "GET":
        return redirect(url_for("admin.blog_list"))
    else:
        data = request.get_json()
        if len(data["article"]) != 0:
            for article_id in data["article"]:
                content = Article.query.filter(
                    Article.id == article_id).first()
                if content.delete():
                    print("ok")
            content_list = Article.query.all()
            data_list = []
            for data in content_list:
                data_list.append(data.to_json())
            current_app.logger.info("文章删除成功")
            return jsonify(data_list)
        return jsonify({"ok": "ok"})
# 删除文章


@admin.route("/admin/blog-set/", methods=["GET", "POST","PUT"])
# 博客设置
@login_required
def blog_set():
    if request.method == "GET":
        return render_template("blog-set.html")
    elif request.method == "POST":

        data = current_app.config["INFO"]
        return jsonify(data)
    elif request.method == "PUT":
        from config.rw_json import write_json
        data = request.get_json().get('data')
        print(data)
        write_json(data)
        current_app.config["INFO"] = data
        current_app.logger.info("博客配置修改成功")
        return jsonify(data)


@admin.route('/admin/comment/', methods=['POST', "GET", "DELETE"])
# 博客评论管理
@login_required
def blog_comment():
    if request.method == "GET":
        return render_template("blog-comment.html", **locals())
    elif request.method == "POST":
        comments = Comment.query.all()
        data = []
        for comment in comments:
            data.append({"created": str(comment.created),
                         "id": comment.id,
                         "web_site": comment.web_site,
                         "text": comment.text,
                         "guest_email": comment.guest_email,
                         "guest_name": comment.guest_name,
                         "post_id": comment.post_id,
                         "uuid": comment.uuid})
        return jsonify(data)

    elif request.method == "DELETE":
        deleted_list = request.get_json()
        status = {"success": 0, "error": 0}
        print(deleted_list.get("delete_list"))
        for data in deleted_list.get("delete_list"):

            comment = Comment.query.filter(
                Comment.id == data.get("id")
            ).first()
            print(comment)
            if comment.delete():
                status["success"] += 1
            else:
                status["error"] += 1
        comments = Comment.query.all()
        data = []
        for comment in comments:
            data.append({"created": str(comment.created),
                         "id": comment.id,
                         "web_site": comment.web_site,
                         "text": comment.text,
                         "guest_email": comment.guest_email,
                         "guest_name": comment.guest_name,
                         "post_id": comment.post_id,
                         "uuid": comment.uuid})
        current_app.logger.info("评论删除成功")
        return jsonify({"data": data, "status": status})


@admin.route('/admin/log/', methods=['GET', 'POST'])
@login_required
# 博客日志
def blog_log():
    if request.method == "GET":
        return render_template('blog-log.html', **locals())
    else:
        logData = []
        path = 'FlyBlog.log'
        with open(path, "r") as f:
            for line in f:
                logData.append(line)
        return jsonify({'data': logData})


@admin.route('/admin/py-link/', methods=['GET'])
# 博客友链管理
@login_required
def py_link():

    return render_template('blog-link.html', **locals())


@admin.route('/admin/py-link/handle', methods=['POST', 'GET', 'PUT', 'DELETE'])
# 博客友链方法
@login_required
def py_link_handle():
    if request.method == 'GET':
        py_links = PyLink.query.all()
        data = []
        for i in py_links:
            data.append(i.to_json())
        return jsonify(data)
    elif request.method == 'POST':
        blog_data = request.get_json()
        py = PyLink(name=blog_data.get('name'), link=blog_data.get('link'),
                    avatar=blog_data.get('avatar'), brief=blog_data.get('brief'))

        if py.save():
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({'data': data, 'message': 'success'})
        else:
            return jsonify({'message': 'error'})
    elif request.method == "PUT":
        blog_data = request.get_json()
        py = PyLink.query.filter(PyLink.id == blog_data.get('id')).first()
        py.name = blog_data.get('name')
        py.link = blog_data.get('link')
        py.avatar = blog_data.get('avatar')
        py.brief = blog_data.get('brief')
        try:
            db.session.commit()
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({"data": data, 'message': 'success'})
        except:
            return jsonify({'message': "error"})
    elif request.method == "DELETE":
        blog_data = request.get_json()
        py = PyLink.query.filter(PyLink.id == blog_data.get('id')).first()
        if py.delete():
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({'data': data, 'message': 'success'})
        else:
            return jsonify({'message': 'error'})


@admin.route('/admin/category/')
@login_required
def blog_category():
    categoryData = Category.query.all()
    categorys = []
    for i in categoryData:
        categorys.append({'id': i.id, 'name': i.name})
    return render_template('blog-category.html', **locals())


@admin.route('/admin/category/handle', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
# 分类修改方法
def blog_category_handle():
    if request.method == "GET":
        categoryData = Category.query.all()
        categorys = []
        for i in categoryData:
            categorys.append({'id': i.id, 'name': i.name})
        return jsonify(categorys)
    elif request.method == "POST":
        category = Category(name=request.get_json().get('category'))
        db.session.add(category)
        db.session.commit()
        categoryData = Category.query.all()
        categorys = []
        for i in categoryData:
            categorys.append({'id': i.id, 'name': i.name})
        return jsonify(categorys)
    elif request.method == "PUT":
        data = request.get_json().get('category')
        category = Category.query.filter_by(id=data.get('id')).first()
        category.name = data.get('name')
        if category.updata():

            categoryData = Category.query.all()
            categorys = []
            for i in categoryData:
                categorys.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "success",
                            "message": ' 修改成功！', 'data': categorys})
        else:
            categoryData = Category.query.all()
            categorys = []
            for i in categoryData:
                categorys.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "error",
                            "message": ' 修改失败！', 'data': categorys})
