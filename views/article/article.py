from flask import url_for, render_template, Blueprint, request, jsonify, redirect,\
    session, current_app, send_from_directory, make_response
from flask_paginate import Pagination
from models.Content import Article, Tag, Category
from models.User import User
from models.Commet import Comment
from models.Other import PyLink
from datetime import datetime
from tool import login_required, sys_name, get_month_range, get_month_days
from extension import scheduler, search, csrf
import requests
import os
from datetime import timedelta
article = Blueprint("article", __name__,
                    template_folder="../../views/article/templates/",
                    static_folder="../../views/article/static/",
                    static_url_path="/article/"
                    )

# 首页


@article.route("/home/")
@article.route("/")
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
        category = c.category[0].name
        data = {'category': category, "url_en": c.url_en,
                'created': c.created, 'slug': c.slug, 'title': c.title}
        articles.append(data)
    contents = articles
    return render_template("home.html", **locals())

# 文章


@article.route("/article/<int:url>")
@article.route("/article/<url>")
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
        print(articleList)
        nextPage = articleList[articleList.index(
            url)+1] if len(articleList) > articleList.index(
            url)+1 else False
        prevPage = articleList[articleList.index(
            url)-1] if 0 <= articleList.index(
            url)-1 else False
        content = Article.query.filter_by(id=url).first_or_404()
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
        return redirect(url_for('admin.blog_info'))
    info = current_app.config.get("INFO")
    if request.method == "GET":
        return render_template("login.html", **locals())
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter(User.mail == email).first()
        if user:

            if user.check_password(password):
                session['username'] = user.showName
                session['email'] = user.mail
                session['user_id'] = user.id
                session['type'] = 'admin'
                session['commet_name'] = user.showName
                session['commet_email'] = user.mail
                if request.form.get("remember"):
                    session.permanent = True
                    current_app.permanent_session_lifetime = timedelta(
                        minutes=24*60*7)
                current_app.logger.info("登陆博客成功")
                return redirect(url_for("admin.blog_info"))
            else:
                current_app.logger.info("登陆博客失败")
                return redirect(url_for("article.login"))
        else:
            # 密码或者用户名错误
            current_app.logger.info("登陆博客失败")
            return redirect(url_for("article.login"))


@article.route("/category/<category>/")
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
    contents = data.articles
    return render_template("category.html", **locals())


@article.route("/about/")
# 关于
def about():
    return render_template("about.html", **locals())


@article.route("/robots.txt/")
# robots.txt
def robots():
    if sys_name() == "Windows":
        path = r"..\views\article\static"
    else:
        path = "../views/article/static"
    return send_from_directory(path, 'robots.txt')
    # return "aaa"


@article.route("/sitemap.xml/")
def sitemap():
    if sys_name() == "Windows":
        path = r"..\views\article\static"
    else:
        path = "../views/article/static"
    return send_from_directory(path, "sitemap.xml")


@article.app_errorhandler(404)
# 404错误
def server_404(e):
    current_app.logger.info("404错误")
    return render_template("404.html"), 404


@article.app_errorhandler(500)
# 500错误
def server_500(e):
    current_app.logger.info("500错误")
    return render_template("500.html"), 500


@article.route("/logout/", methods=["GET", "POST"])
# 退出登录
@login_required
# 退出登录
def logout():
    current_app.logger.info("退出登陆")
    session.clear()
    return redirect(url_for("article.home"))


@article.route("/archive/", methods=["GET"])
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
    print(request.method)
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
                if review.save():
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': '服务器发生错误！'})
            else:

                review = Comment(post_id=article_id, user_id=user_id,
                                 agent=agent, comment_type=comment_type,
                                 guest_name=nick, guest_email=mail,
                                 text=text, web_site=link,
                                 show_status=True)
                if review.save():
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'status': 'error', 'message': '服务器发生固执'})
        else:
            return {'status': 'error', 'message': '验证码错误'}

    return 'aa'


@article.route("/interval/")
# 站点地图半小时刷新
def interval_job():
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
            data = "<url>\n" + "<loc>http://{}/article/{}</loc>".format(
                "www.gynl.xyz", content.url_en) + "\n" + \
                "<lastmod>{}</lastmod>".format(content.modified)+"\n" +\
                "<priority>0.8</priority>" + "\n" + "</url>" + "\n"
            data_contents = data_contents + data
        xml_contents = header + "\n" + data_contents + "\n" + footer
        f.write(xml_contents)

    return "ok"


@scheduler.task('interval', id='do_job_1', seconds=1800)
def job1():
    date = requests.get("http://127.0.0.1:5000/interval/")
    print(date)
    # 循环任务，每30min秒循环一次


@article.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        info = current_app.config.get("INFO")
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
def tags():
    # 标签云
    info = current_app.config.get("INFO")
    tags = Tag.query.all()
    return render_template("tag.html", **locals())


@article.route("/tag/<url>", methods=["GET"])
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
    print(contents)
    return render_template("home.html", **locals())


@article.route("/py-link/")
def py_link():
    # 友情链接
    info = current_app.config.get("INFO")
    pys = PyLink.query.all()
    return render_template("py-link.html", **locals())


@article.route("/message/")
def message():
    # 留言
    info = current_app.config.get("INFO")
    comments = Comment.query.order_by(
        Comment.created.desc()).filter_by(comment_type='message').all()
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
