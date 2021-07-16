from extension import bcrypt, db
from flask import (Blueprint, current_app, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_wtf.csrf import generate_csrf
from models.Commet import Comment
from models.Content import Article, Category, Tag
from models.Other import PyLink, View
from models.User import User
from tool import (Md5, get_server_info, login_required,
                  sys_name, get_cur_month_end, get_cur_month_start,
                  getAnalyTime)
from datetime import datetime

admin = Blueprint("admin", __name__,
                  template_folder="../../views/admin/templates/",
                  static_folder="../../views/admin/static/",
                  static_url_path="/admin/"
                  )


@admin.route("/admin/dashboard/", methods=['GET', "POST"])
@login_required
# 博客信息
def blog_dashboard():
    if request.method == 'GET':
        return render_template("blog-dashboard.html")
    else:
        data = get_server_info()
        start = get_cur_month_start()
        end = get_cur_month_end()
        comment = Comment.query.filter(
            Comment.created <= end).filter(Comment.created
                                           >= start).count()
        commentData = Comment.query.order_by(
            Comment.created.desc()).slice(0, 10)
        comments = []
        for i in commentData:
            comments.append({'text': i.text, 'created': i.created})
        articleData = Article.query.order_by(
            Article.created.desc()).slice(0, 10)
        articles = []
        for i in articleData:
            articles.append({'title': i.title, 'created': i.created})
        view = View.query.filter_by(created=getAnalyTime()).first()
        view = view if view else 0
        viewData = View.query.order_by(
            View.created.desc()).slice(0, 7)
        print(viewData)
        views = []
        for i in viewData:
            views.append(
                {'mun': i.views, 'day': datetime.strftime(i.created, '%m-%d')})
        views.reverse()
        return jsonify({'data':
                        {'disk': data.get('disk_used')+'/'+data.get('disk_total'),
                         'memory': data.get('memory_used')+'/'+data.get('memory_total'),
                         'comment': comment, 'comments': comments, 'articles': articles,
                         'views': view.views, 'timeData': views}})


@admin.route("/admin/blog-write/", methods=["POST", "GET"])
@login_required
# 创建新文章
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
        for i in tags:
            blogTag = Tag().query.filter(Tag.name == i).first()
            if blogTag:
                article.tags.append(blogTag)
                db.session.add(blogTag)
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
        save = article.save()
        if save.get('status'):
            return jsonify({'status': "success", 'message': '文章修改成功'})
        else:
            return jsonify({'status': "error", 'message':str(save.get('message'))})
    else:
        return render_template("blog-write.html", **locals())


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
        if len(data["article"]) != 0:
            for article_id in data["article"]:
                content = Article.query.filter(
                    Article.id == article_id.get('id')).first()
                delete = content.delete()
                if delete.get('status'):
                    content_list = Article.query.all()
                    data_list = []
                    for data in content_list:
                        data_list.append(data.to_json())
                    return jsonify({'status': "success",
                                    "message": ' 删除成功！', 'data': data_list})
                else:
                    return jsonify({'status': "error", "message": str(delete.get("message"))})

        return jsonify({"ok": "ok"})


@admin.route("/admin/blog-modify/<int:url>", methods=["GET", "POST", "PUT"])
@login_required
# 修改文章
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
        content.text = text
        content.url_en = url_en
        content.image_url = image_url
        content.template = template
        updata = content.updata()
        if updata.get('status'):
            return jsonify({'status': "success",
                            "message": ' 修改成功！'})

        else:
            return jsonify({'status': "error",
                            "message": str(updata.get('message'))})

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


@admin.route("/admin/blog-delete/", methods=["GET", "POST"])
@login_required
# 删除文章
def blog_delete():
    if request.method == "GET":
        return redirect(url_for("admin.blog_list"))
    else:
        data = request.get_json()
        if len(data["article"]) != 0:
            for article_id in data["article"]:
                content = Article.query.filter(
                    Article.id == article_id).first()
                delete = content.delete()
                if delete.get('status'):
                    print("ok")
            content_list = Article.query.all()
            data_list = []
            for data in content_list:
                data_list.append(data.to_json())
            return jsonify(data_list)
        return jsonify({"ok": "ok"})


@admin.route("/admin/blog-set/", methods=["GET", "POST", "PUT"])
# 博客设置
@login_required
def blog_set():
    if request.method == "GET":
        return render_template("blog-set.html")
    elif request.method == "POST":
        data = current_app.config["INFO"]
        user = User.query.filter(User.id == session.get('user_id')).first()
        return jsonify({'data': data, 'username': user.username, 'email': user.mail})
    elif request.method == "PUT":
        data = request.get_json().get('data')
        info = current_app.config["INFO"]
        if request.get_json().get('type') == 'userInfo':
            user = User.query.filter(User.id == session.get('user_id')).first()
            if data.get('oldPassword') and data.get('newPassword'):  # 新旧密码存在
                if user.check_password(data.get('oldPassword')):
                    user.password = bcrypt.generate_password_hash(
                        data.get('newPassword'))
                else:
                    return jsonify({'status': "error",
                                    "message": ' 密码错误！'})
            user.username = data.get('username')
            user.mail = data.get('email')
            updata = user.updata()
            if updata.get('status'):
                info['other']['email'] = Md5(data.get('email'))
                # 修改email的hash
                from config.rw_json import write_json
                write_json(info)
                return jsonify({'status': "success",
                                "message": ' 修改用户信息成功！'})
            else:
                return jsonify({'status': "error",
                                "message": str(updata.get('message'))})
        elif request.get_json().get('type') == 'blogConfig':
            from config.rw_json import write_json
            data = request.get_json().get('data').get('data')
            current_app.config["INFO"] = data
            write_json(current_app.config["INFO"])
            return jsonify({'status': "success", "message": ' 修改用成功！'})


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
            delete = comment.delete()
            if delete.get('status'):
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
        return jsonify({"data": data, "status": status})


@admin.route('/admin/log/', methods=['GET', 'POST', "DELETE"])
@login_required
# 博客日志
def blog_log():
    if request.method == "GET":
        return render_template('blog-log.html', **locals())
    elif request.method == "POST":
        logData = []
        path = 'FlyBlog.log'
        with open(path, "r") as f:
            for line in f:
                logData.append(line)
        return jsonify({'data': logData})
    elif request.method == "DELETE":
        logData = ''
        path = 'FlyBlog.log'
        with open(path, "w+") as f:
            f.write(logData)
        return jsonify({'data': []})


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
        save = py.save()
        if save.get('status'):
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({'data': data, 'message': 'success'})
        else:
            return jsonify({'message': str(save.get('message'))})
    elif request.method == "PUT":
        blog_data = request.get_json()
        py = PyLink.query.filter(PyLink.id == blog_data.get('id')).first()
        py.name = blog_data.get('name')
        py.link = blog_data.get('link')
        py.avatar = blog_data.get('avatar')
        py.brief = blog_data.get('brief')
        updata = py.updata()
        if updata.get('status'):
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({"data": data, 'message': 'success'})
        else:
            return jsonify({'message': str(updata.get('message'))})
    elif request.method == "DELETE":
        blog_data = request.get_json()
        py = PyLink.query.filter(PyLink.id == blog_data.get('id')).first()
        delete = py.delete()
        if delete.get('status'):
            py_links = PyLink.query.all()
            data = []
            for i in py_links:
                data.append(i.to_json())
            return jsonify({'data': data, 'message': 'success'})
        else:
            return jsonify({'message': str(delete.get('message'))})


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
        save = category.save()
        if save.get('status'):
            categoryData = Category.query.all()
            categorys = []
            for i in categoryData:
                categorys.append({'id': i.id, 'name': i.name})
            return jsonify(categorys)
        else:
            return jsonify({'message':str(save.get('message'))})
    elif request.method == "PUT":
        data = request.get_json().get('category')
        category = Category.query.filter_by(id=data.get('id')).first()
        category.name = data.get('name')
        updata = category.updata()
        if updata.get('status'):
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
                            "message": str(updata.get('message')), 'data': categorys})
    elif request.method == "DELETE":
        id = request.get_json().get('id')
        category = Category.query.filter_by(id=id).first()
        delete = category.delete()
        if delete.get('status'):
            categoryData = Category.query.all()
            categorys = []
            for i in categoryData:
                categorys.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "success",
                            "message": ' 修改成功！', 'data': categorys})
    return jsonify({'status': "error",
                    "message": str(delete.get('message'))})


@admin.route('/admin/tag', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
# 文章标签
def blog_tag():
    if request.method == "GET":
        return render_template('blog-tag.html', **locals())
    elif request.method == "POST":
        tagData = Tag.query.all()
        tags = []
        for i in tagData:
            tags.append({'id': i.id, 'name': i.name})
        return jsonify(tags)
    elif request.method == "PUT":
        data = request.get_json().get('tag')
        tag = Tag.query.filter_by(id=data.get('id')).first()
        tag.name = data.get('name')
        updata = tag.updata()
        if updata.get('status'):
            tagData = Tag.query.all()
            tags = []
            for i in tagData:
                tags.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "success",
                            "message": ' 修改成功！', 'data': tags})
        else:
            tagData = Tag.query.all()
            tags = []
            for i in tagData:
                tags.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "error",
                            "message": str(updata.get('message')), 'data': tags})
    elif request.method == "DELETE":
        id = request.get_json().get('id')
        tag = Tag.query.filter_by(id=id).first()
        delete = tag.delete()
        if delete.get('status'):
            tagData = Tag.query.all()
            tags = []
            for i in tagData:
                tags.append({'id': i.id, 'name': i.name})
            return jsonify({'status': "success",
                            "message": ' 修改成功！', 'data': tags})
        else:
            return jsonify({'status': "error",
                            "message": str(delete.get('message'))})

@admin.route('/admin/about', methods=['POST', 'GET', 'PUT'])
@login_required
def blog_about():
    '''关于Script && Meta'''
    if request.method == "GET":
        return render_template('blog-about.html')

    elif request.method == 'POST':
        script = ''
        if sys_name() == "Windows":
            path = r".\views\article\templates\include\script.html"
        else:
            path = "./views/article/templates/include/script.html"
        with open(path, 'r+') as f:
            script = f.read()
        meta = ''
        if sys_name() == "Windows":
            path = r".\views\article\templates\include\meta.html"
        else:
            path = "./views/article/templates/include/meta.html"
        with open(path, 'r+') as f:
            meta = f.read()
        return jsonify({'script': script, 'meta': meta})
    elif request.method == "PUT":
        script = request.get_json().get('script')
        script = script if script else ""
        meta = request.get_json().get('meta')
        meta = meta if meta else ""
        if sys_name() == "Windows":
            path = r".\views\article\templates\include\script.html"
        else:
            path = "./views/article/templates/include/script.html"
        with open(path, 'w+') as f:
            script = f.write(script)
        if sys_name() == "Windows":
            path = r".\views\article\templates\include\meta.html"
        else:
            path = "./views/article/templates/include/meta.html"
        with open(path, 'w+') as f:
            meta = f.write(meta)
        return jsonify({'status': "success",
                        "message": ' 修改成功！'})


