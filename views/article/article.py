from array import array
from email import header
from flask import url_for, render_template, Blueprint, request, jsonify, redirect,\
    session, current_app, send_from_directory, make_response
from flask.wrappers import Response
from flask_paginate import Pagination
from sqlalchemy import not_, or_
from sqlalchemy.sql.expression import null
from models.Content import Article, Tag, Category
from models.User import User
from models.Commet import Comment
from models.Other import PyLink
from datetime import datetime, time, timezone
from tool import login_required, sys_name, get_month_range, get_month_days, Md5,\
    cache_key
from extension import scheduler, search, csrf, cache
from datetime import timedelta
article = Blueprint("article", __name__,
                    template_folder="../../views/article/templates/",
                    static_folder="../../views/article/static/",
                    static_url_path=''
                    )


@article.route("/")
@article.route('/index/')
# @cache.cached(make_cache_key=cache_key)
# 首页
def home():
    info = current_app.config.get("INFO")
    page = request.args.get("page", type=int, default=1)
    page_content = info.get('blogConfig').get('articleItem')
    total = Article.query.count()
    start = (page-1)*page_content
    end = start + page_content
    pagination = Article.query.order_by(Article.created.desc()).paginate(
        page, per_page=page_content, error_out=False)
    contents = Article.query.order_by(Article.created.desc()).slice(start, end)
    articles = []
    for c in contents:
        category = c.category[0].name if len(c.category.all()) > 0 else '未分类'
        data = {'category': category, "url_en": c.url_en,
                'created': c.created, 'slug': c.slug, 'title': c.title,
                'image_url': c.image_url}
        articles.append(data)
    contents = articles
    return render_template("home.html", **locals())

# 文章


@article.route("/article/<int:url>")
@article.route("/article/<url>")
@cache.cached()
def post(url):
    pages = []
    posts = Article.query.all()
    if type(url) == type("str"):
        articleList = [i.url_en for i in posts]
        nextPage = articleList[articleList.index(
            url)+1] if len(articleList) > articleList.index(
            url)+1 else False
        prevPage = articleList[articleList.index(
            url)-1] if 0 <= articleList.index(
            url)-1 else False
        content = Article.query.filter_by(url_en=url).first_or_404()
        user = User.query.filter(User.id == content.user_id).first()
        comments = Comment.query.order_by(
            Comment.created.desc()).filter_by(post_id=content.id).all()
        comment_data = []
        comment_mun = 0
        for comment in comments:
            comment_mun += 1
            c_comments = Comment.query.order_by(
                Comment.created.desc()).filter_by(parent_uuid=comment.uuid).all()
            c_comment_data = []

            for c_comment in c_comments:
                comment_mun += 1
                text = c_comment.text if c_comment.show_status else "该评论未允许显示！"
                c_comment_data.append({'nick': c_comment.guest_name,
                                       'link': c_comment.web_site,
                                       'uuid': c_comment.uuid,
                                       'text': text,
                                       'agent': c_comment.agent,
                                       'hash_email': c_comment.hash_email,
                                       'created': c_comment.created,
                                       'parent_uuid': c_comment.parent_uuid,
                                       'parent_name': c_comment.parent_name})
            text = comment.text if comment.show_status else "该评论未允许显示！"
            comment_data.append({
                'nick': comment.guest_name,
                'link': comment.web_site,
                'uuid': comment.uuid,
                'text': text,
                'agent': comment.agent,
                'hash_email': comment.hash_email,
                'created': comment.created,
                'parent_id': comment.id,
                'c_comment_data': c_comment_data
            })
        return render_template("article.html", **locals())
    else:
        articleList = [i.id for i in posts]
        nextPage = articleList[articleList.index(
            url)+1] if len(articleList) > articleList.index(
            url)+1 else False
        prevPage = articleList[articleList.index(
            url)-1] if 0 <= articleList.index(
            url)-1 else False
        content = Article.query.filter_by(id=url).first_or_404()
        user = User.query.filter_by(id=content.user_id).first()
        comments = Comment.query.order_by(
            Comment.created.desc()).filter_by(post_id=content.id).all()
        comment_data = []
        comment_mun = 0
        for comment in comments:
            comment_mun += 1
            c_comments = Comment.query.order_by(
                Comment.created.desc()).filter_by(parent_uuid=comment.uuid).all()
            c_comment_data = []
            for c_comment in c_comments:
                comment_mun += 1
                text = c_comment.text if c_comment.show_status else "该评论未允许显示！"
                c_comment_data.append({'nick': c_comment.guest_name,
                                       'link': c_comment.web_site,
                                       'uuid': c_comment.uuid,
                                       'text': text,
                                       'agent': c_comment.agent,
                                       'hash_email': c_comment.hash_email,
                                       'created': c_comment.created,
                                       'parent_uuid': c_comment.parent_uuid,
                                       'parent_name': c_comment.parent_name})
            text = comment.text if comment.show_status else "该评论未允许显示！"
            comment_data.append({
                'nick': comment.guest_name,
                'link': comment.web_site,
                'uuid': comment.uuid,
                'text': text,
                'agent': comment.agent,
                'hash_email': comment.hash_email,
                'created': comment.created,
                'parent_id': comment.id,
                'c_comment_data': c_comment_data
            })
        return render_template("article.html", **locals())


@csrf.exempt
@article.route("/login/", methods=["GET", "POST"])
# 登录
def login():
    if session.get("username"):
        return redirect(url_for('admin.blog_dashboard'))
    if request.method == "GET":
        return render_template("login.html", **locals())
    else:
        data = request.get_json().get('data')
        user = User.query.filter(User.mail == data.get('email')).first()
        if user:
            if user.check_password(data.get('password')):
                session['username'] = user.showName
                session['email'] = user.mail
                session['user_id'] = user.id
                session['type'] = 'admin'
                session['commet_name'] = user.showName
                session['commet_email'] = user.mail
                if data.get("remember"):
                    session.permanent = True
                    current_app.permanent_session_lifetime = timedelta(
                        minutes=24*60*7)
                current_app.logger.info("登陆博客成功")
                return jsonify({'status': "success",
                                "message": '登陆成功，欢迎回来！'})
            else:
                current_app.logger.warning("登陆博客失败-密码错误")
                return jsonify({'status': "error",
                                "message": '密码或者用户名错误！'})
        else:
            # 密码或者用户名错误
            current_app.logger.warning("登陆博客失败-户名错误")
            return jsonify({'status': "error",
                            "message": '密码或者用户名错误！'})


@article.route("/register/", methods=["GET", "POST"])
# 注册
def register():
    info = current_app.config["INFO"]
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        if info.get('blogConfig').get('register'):
            data = request.get_json().get('data')
            user = User(username=data.get('username'), mail=data.get(
                'email'), password=data.get('password'))
            save = user.save()
            if save.get('status'):
                info['other']['email'] = Md5(data.get('email'))
                # 修改email的hash
                from config.rw_json import write_json
                write_json(info)
                return jsonify({'status': "success",
                                "message": '注册成功……即将转跳！'})
            else:
                return jsonify({'status': "error",
                                "message": save.get('message')})
        else:
            return jsonify({'status': "error",
                            "message": '已经关闭注册！'})


@article.route("/category/<category>/")
@cache.cached()
# 文章分类
def category(category):
    info = current_app.config.get("INFO")
    page = request.args.get("page", type=int, default=1)
    pageItem = info.get('blogConfig').get('articleItem')
    data = Category.query.filter_by(
        name=category).first_or_404()
    articleData = data.articles
    start = (page-1)*pageItem
    end = start + pageItem
    pagination = articleData.order_by(Article.created.desc()).paginate(
        page, per_page=pageItem, error_out=False)
    contents = articleData.order_by(Article.created.desc()).slice(start, end)
    # contents = data.articles
    print(contents)
    return render_template("category.html", **locals())


@article.route("/about/")
# 关于
def about():
    return render_template("about.html", **locals())


@article.route('/favicon.ico')
def favicon():
    if sys_name() == "Windows":
        path = r"..\views\article\static"
    else:
        path = "../views/article/static"
    return send_from_directory(path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@article.route("/robots.txt")
# robots.txt
def robots():
    info = current_app.config.get("INFO")
    robots = "User-agent: * \n"\
        "Disallow: /admin/\n"\
        "Disallow: /login/\n"\
        "Sitemap: {}/sitemap.xml".format(
            info.get('blogConfig').get('domainName'))
    response = make_response(robots)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response


@article.route('/sitemap.xml')
def sitemap():
    if sys_name() == "Windows":
        path = r"views\article\static\sitemap.xml"
    else:
        path = "views/article/static/sitemap.xml"
    # data = send_from_directory(article.static_folder, request.path[1:])
    response = make_response(open(path).read())
    response.headers['Content-Type'] = 'application/xml'
    return response


@article.app_errorhandler(404)
# 404错误
def server_404(e):
    current_app.logger.warning("404错误:访问页面不存在")
    return render_template("404.html"), 404


@article.app_errorhandler(500)
# 500错误
def server_500(e):
    current_app.logger.exception("500错误:------------------------")
    return render_template("500.html"), 500


@article.route("/logout/", methods=["GET", "POST"])
# 退出登录
@login_required
def logout():
    current_app.logger.info("退出登陆")
    session.clear()
    return redirect(url_for("article.home"))


@article.route("/archive/", methods=["GET"])
@cache.cached()
# 归档数据
def archive():
    info = current_app.config.get("INFO")
    if request.method == "GET":
        content_start = Article.query.first()
        startTime = content_start.created
        content_end = Article.query.order_by(Article.created.desc()).first()
        endTime = content_end.created
        times = get_month_range(startTime, endTime)
        contentData = []
        right = True
        for i in range(len(times)):
            right = bool(1-right)
            content = Article.query.filter(
                Article.created >
                datetime.strptime(times[i], "%Y-%m")).filter(
                Article.created <
                datetime.strptime(times[i], "%Y-%m")+timedelta(days=get_month_days(times[i]))).order_by(Article.created.desc())
            contentData.append(
                {'num': content.count(), 'articles': content.all(), 'time': times[i], 'right': right})
        return render_template("archive.html", **locals())
    else:
        data = request.get_json()

        contents = Article.query.filter(
            Article.created >=
            datetime.strptime(data["start"], "%Y-%m")).filter(
            Article.created <
            datetime.strptime(data["end"], "%Y-%m")).order_by(Article.created.desc()).all()
        data_list = []
        for data1 in contents:
            exampleData = {"created": data1.created,
                           "id": data1.id, "title": data1.title}
            data_list.append(exampleData)
        return jsonify(data_list)


@csrf.exempt
@article.route("/comment/", methods=["POST", "GET"])
# 评论
def comment():
    if request.method == "POST":
        if session.get('imageCode').lower() == request.form.get('captcha').lower():
            nick = request.form.get('nick')
            mail = request.form.get('mail')
            text = request.form.get('text')
            link = request.form.get('link')
            comment_type = request.form.get('type')
            parent_id = 0  # 空
            article_id = request.form.get('articleId')
            user_id = request.form.get('userId')
            agent = request.user_agent.browser
            parent_uuid = request.form.get('parent_uuid')
            parent_name = request.form.get('parent_name')

            if parent_uuid:
                review = Comment(user_id=user_id,
                                 agent=agent, comment_type=comment_type,
                                 guest_name=nick, guest_email=mail,
                                 text=text, web_site=link,
                                 show_status=True, parent_uuid=parent_uuid,
                                 parent_name=parent_name, parent_id=parent_id)
                save = review.save()
                if save.get('status'):
                    cache.clear()
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': '服务器发生错误'})
            else:

                review = Comment(post_id=article_id, user_id=user_id,
                                 agent=agent, comment_type=comment_type,
                                 guest_name=nick, guest_email=mail,
                                 text=text, web_site=link,
                                 show_status=True)
                save = review.save()
                if save.get('status'):
                    cache.clear()
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': '服务器发生错误'})
        else:
            return {'status': 'error', 'message': '验证码错误'}

    return 'aa'


@scheduler.task('interval', id='do_job_1', seconds=1800)
# 站点地图更新任务，30min一次
def siteMap():
    with scheduler.app.app_context():
        info = current_app.config.get("INFO")
        contents = Article.query.all()
        header = '<?xml version="1.0" encoding="UTF-8"?> ' + '\n' + \
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        footer = '</urlset>'
        data_contents = ""
        if sys_name() == "Windows":
            path = r".\views\article\static\sitemap.xml"
        else:
            path = "./views/article/static/sitemap.xml"
        with open(path, "w+") as f:
            for content in contents:
                data = "<url>\n" + "<loc>{}/article/{}</loc>".format(
                    info.get('blogConfig').get('domainName'), content.url_en) + "\n" + \
                    "<lastmod>{}</lastmod>".format(content.modified)+"\n" +\
                    "<priority>0.8</priority>" + "\n" + "</url>" + "\n"
                data_contents = data_contents + data
            xml_contents = header + "\n" + data_contents + "\n" + footer
            f.write(xml_contents)
            current_app.logger.info("更新站点地图任务完成")


@article.route("/search/<keyword>/", methods=["GET", "POST"])
def search(keyword):
    if request.method == "GET":
        info = current_app.config.get("INFO")
        print(keyword)
        page = request.args.get("page", type=int, default=1)
        page_content = info.get('blogConfig').get('articleItem')
        total = Article.query.msearch(keyword).count()
        start = (page-1)*page_content
        end = start + page_content
        pagination = Article.query.msearch(keyword).order_by(Article.created.desc()).paginate(
            page, per_page=page_content, error_out=False)
        contents = Article.query.msearch(keyword).order_by(
            Article.created.desc()).slice(start, end)
        articles = []
        for c in contents:
            category = c.category[0].name if len(
                c.category.all()) > 0 else '未分类'
            data = {'category': category, "url_en": c.url_en,
                    'created': c.created, 'slug': c.slug,
                    'title': c.title, 'image_url': c.image_url}
            articles.append(data)
        contents = articles
        return render_template("search.html", **locals())
    else:
        keyword = request.get_json()
        print(keyword.get("search_content"))
        posts = Article.query.msearch(
            keyword.get("search_content"), limit=20).all()
        data = []
        for post in posts:
            data.append({"title": post.title,
                         "id": post.id,
                         "slug": post.slug,
                         "created": post.created})
        return jsonify(data)


@article.route("/tags/", methods=["GET"])
@cache.cached()
def tags():
    # 标签云
    info = current_app.config.get("INFO")
    tags = Tag.query.all()
    return render_template("tags.html", **locals())


@article.route("/tag/<url>", methods=["GET"])
@cache.cached()
def tag(url):
    # 标签页面
    info = current_app.config.get("INFO")
    page = request.args.get("page", type=int, default=1)
    pageItem = info.get('blogConfig').get('articleItem')
    tag = Tag.query.filter(Tag.name == url).first()
    articleData = tag.articles
    start = (page-1)*pageItem
    end = start + pageItem
    pagination = articleData.order_by(Article.created.desc()).paginate(
        page, per_page=pageItem, error_out=False)
    contents = articleData.order_by(Article.created.desc()).slice(start, end)
    articles = []
    for c in contents:
        category = c.category[0].name if len(c.category.all()) > 0 else '未分类'
        data = {'category': category, "url_en": c.url_en,
                'created': c.created, 'slug': c.slug, 'title': c.title}
        articles.append(data)
    contents = articles
    return render_template("tag.html", **locals())


@article.route("/py-link/")
@cache.cached()
def py_link():
    # 友情链接
    info = current_app.config.get("INFO")
    pys = PyLink.query.all()
    return render_template("py-link.html", **locals())


@article.route("/message/")
@cache.cached()
def message():
    # 留言
    info = current_app.config.get("INFO")
    comments = Comment.query.order_by(
        Comment.created.desc()).filter_by(comment_type='message').filter(
            not_(Comment.parent_name != None)).all()
    comment_data = []
    comment_mun = 0
    for comment in comments:
        comment_mun += 1
        c_comments = Comment.query.order_by(
            Comment.created.desc()).filter_by(parent_uuid=comment.uuid).all()
        c_comment_data = []

        for c_comment in c_comments:
            comment_mun += 1
            text = c_comment.text if c_comment.show_status else "该评论未允许显示！"
            c_comment_data.append({'nick': c_comment.guest_name,
                                   'link': c_comment.web_site,
                                   'uuid': c_comment.uuid,
                                   'text': text,
                                   'agent': c_comment.agent,
                                   'hash_email': c_comment.hash_email,
                                   'created': c_comment.created,
                                   'parent_uuid': c_comment.parent_uuid,
                                   'parent_name': c_comment.parent_name})
        text = comment.text if comment.show_status else "该评论未允许显示！"
        comment_data.append({
            'nick': comment.guest_name,
            'link': comment.web_site,
            'uuid': comment.uuid,
            'text': text,
            'agent': comment.agent,
            'hash_email': comment.hash_email,
            'created': comment.created,
            'parent_id': comment.id,
            'c_comment_data': c_comment_data
        })
    return render_template("message.html", **locals())
