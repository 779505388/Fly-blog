from flask import url_for, render_template, Blueprint, request, jsonify, redirect,\
    session, current_app, send_from_directory, make_response
from flask_paginate import Pagination
from models.Content import Content
from models.User import User
from models.Commet import ParentComment, ChildrenCommet
from datetime import datetime
from tool import login_required, sys_name
from extension import scheduler, search
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
    page_content = 10
    total = Content.query.count()
    start = (page-1)*page_content
    end = start + page_content
    pagination = Pagination(bs_version=3, page=page, total=total)
    contents = Content.query.order_by(Content.created.desc()).slice(start, end)
    return render_template("home.html", **locals())

# 文章


@article.route("/article/<int:url>")
@article.route("/article/<url>")
def post(url):
    pages = []
    posts = Content.query.all()
    for post in posts:
        pages.append(post.id)
    info = current_app.config.get("INFO")
    if type(url) == type("str"):
        return render_template("article.html")
    else:
        content = Content.query.filter_by(id=url).first_or_404()
        return render_template("article.html", **locals())


@article.route("/login/", methods=["GET", "POST"])
# 登录
def login():
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
                return redirect(url_for("admin.blog_info"))
            else:
                return redirect(url_for("article.login"))
        else:
            # 密码或者用户名错误
            return redirect(url_for("article.login"))


@article.route("/post/category/<category>/")
# 文章分类
def category(category):
    info = current_app.config.get("INFO")
    if category == "学习的日常" or category == "思考的日常" or \
       category == "折腾的日常" or category == "吐槽的日常":
        contents = Content.query.filter_by(
            post_type=category).order_by(
                Content.created.desc()).all()
        return render_template("category.html", **locals())
    else:
        return "404 Not found", 404


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
    return render_template("404.html"), 404


@article.app_errorhandler(500)
# 500错误
def server_500(e):
    return render_template("500.html"), 500


@article.route("/logout/", methods=["GET", "POST"])
# 退出登录
@login_required
# 退出登录
def logout():
    session.clear()
    return redirect(url_for("article.home"))


@article.route("/archive/", methods=["GET", "POST"])
# 归档数据
def archive():
    info = current_app.config.get("INFO")
    if request.method == "GET":
        content_start = Content.query.first()
        startTime = content_start.created
        content_end = Content.query.order_by(Content.created.desc()).first()
        endTime = content_end.created
        return render_template("archive.html", **locals())
    else:
        data = request.get_json()

        contents = Content.query.filter(
            Content.created >=
            datetime.strptime(data["start"], "%Y-%m")).filter(
            Content.created <
            datetime.strptime(data["end"], "%Y-%m")).order_by(Content.created.desc()).all()
        data_list = []
        for data1 in contents:
            exampleData = {"created": data1.created,
                           "id": data1.id, "title": data1.title}
            data_list.append(exampleData)
        return jsonify(data_list)


@article.route("/comment/", methods=["POST", "GET"])
# 评论
def comment():
    if request.method == "GET":
        comments = ParentComment.query.filter_by(
            post_id=request.args.get("post_id")).all()
        comment_list = []
        print(request.args.get("post_id"))
        for comment in comments:
            children_list = []
            for c_comment in comment.children_commets:
                children_list.append(
                    {"guest_name": c_comment.guest_name,
                     "created": str(c_comment.created),
                     "hash_email": c_comment.hash_email,
                     "text": c_comment.text
                     }
                )
            comment_list.append({"guest_name": comment.guest_name,
                                 "created": str(comment.created),
                                 "hash_email": comment.hash_email,
                                 "text": comment.text,
                                 "id": comment.id,
                                 "children_comment": children_list})
        return jsonify(comment_list)
    else:
        data = request.get_json()
        if session.get('imageCode').upper() != data.get('captcha').upper():
            return jsonify({"error": "验证码错误"})
        if data.get("type") == "parent":
            p_comment = ParentComment(guest_email=data.get("guest_email"),
                                      guest_name=data.get("guest_name"),
                                      web_site=data.get("web_site"),
                                      text=data.get("text"),
                                      post_id=data.get("post_id"))
            if p_comment.save():
                comments = ParentComment.query.filter_by(
                    post_id=data.get("post_id")).all()
                comment_list = []
                for comment in comments:
                    children_list = []
                    for c_comment in comment.children_commets:
                        children_list.append(
                            {"guest_name": c_comment.guest_name,
                                "created": str(c_comment.created),
                                "hash_email": c_comment.hash_email,
                                "text": c_comment.text
                             }
                        )
                    comment_list.append({"guest_name": comment.guest_name,
                                         "created": comment.created,
                                         "hash_email": comment.hash_email,
                                         "text": comment.text,
                                         "id": comment.id,
                                         "children_comment": children_list})
                return jsonify(comment_list)
            else:
                return jsonify("提交评论错误")
        elif data.get("type") == "children":
            c_comment = ChildrenCommet(guest_email=data.get("guest_email"),
                                       guest_name=data.get("guest_name"),
                                       web_site=data.get("web_site"),
                                       text=data.get("text"),
                                       post_id=data.get("post_id"),
                                       parent_id=data.get("parent_id"))
            if c_comment.save():
                comments = ParentComment.query.filter_by(
                    post_id=data.get("post_id")).all()
                comment_list = []
                for comment in comments:
                    children_list = []
                    for c_comment in comment.children_commets:
                        children_list.append(
                            {"guest_name": c_comment.guest_name,
                                "created": str(c_comment.created),
                                "hash_email": c_comment.hash_email,
                                "text": c_comment.text
                             }
                        )
                    comment_list.append({"guest_name": comment.guest_name,
                                         "created": comment.created,
                                         "hash_email": comment.hash_email,
                                         "text": comment.text,
                                         "id": comment.id,
                                         "children_comment": children_list})
                return jsonify(comment_list)
        else:
            return jsonify({"error":"评论类型错误"})
        print(request.get_json())
        return jsonify(request.get_json())


@article.route("/interval/")
# 站点地图半小时刷新
def interval_job():
    contents = Content.query.all()
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
                "www.gynl.xyz", content.id) + "\n" + \
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
        posts = Content.query.msearch(
            keyword.get("search_content"), limit=20).all()
        data = []
        for post in posts:
            data.append({"title": post.title,
                         "id": post.id,
                         "slug": post.slug,
                         "created": post.created})
        return jsonify(data)
