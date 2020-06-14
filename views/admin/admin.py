from flask import url_for, render_template, Blueprint, request, session,\
    redirect, jsonify, current_app
from flask_wtf.csrf import generate_csrf
from models.Content import Content
from models.Commet import ParentComment, ChildrenCommet
from tool import get_server_info, login_required
admin = Blueprint("admin", __name__,
                  template_folder="../../views/admin/templates/",
                  static_folder="../../views/admin/static/",
                  static_url_path="/admin/"
                  )


@admin.route("/admin/blog-info/")
@login_required
def blog_info():
    print(session.get("username"))
    return render_template("blog-info.html")
# 博客信息


@admin.route("/admin/blog-write/", methods=["POST", "GET"])
@login_required
def blog_write():
    if request.method == 'POST':
        if request.form.get('csrf_token') == session.get('blog_post_csrf_token'):
            title = request.form.get('title')
            slug = request.form.get('slug')
            tag = request.form.get('tag')
            post_type = request.form.get('type')
            text = request.form.get('editormd')
            url_en = request.form.get("url")
            user_id = 2
            image_url = request.form.get("image")
            template = request.form.get("template")
            content = Content(title=title, slug=slug, user_id=user_id,
                              post_type=post_type, url_en=url_en, tag=tag,
                              image_url=image_url,
                              text=text, template=template
                              )
            if content.save():
                return redirect(url_for("article.home"))
            else:
                return "错误", 302

        else:
            return "错误", 302
    csrf_token = generate_csrf()
    session['blog_post_csrf_token'] = csrf_token
    return render_template("blog-write.html", **locals())
# 创建新文章


@admin.route("/admin/blog-list/", methods=["GET", "POST", "DELETE"])
@login_required
def blog_list():
    if request.method == "GET":
        return render_template("blog-list.html")
    elif request.method == "POST":
        content_list = Content.query.all()
        data_list = []
        for data in content_list:
            data_list.append(data.to_json())
        return jsonify(data_list)
# 文章列表


@admin.route("/admin/blog-modify/<int:url>", methods=["GET", "POST"])
@login_required
def blog_modify(url):
    if request.method == "GET":
        csrf_token = generate_csrf()
        session['blog_modify_csrf_token'] = csrf_token
        content = Content.query.filter_by(id=url).first()
        return render_template("blog-modify.html", **locals())
    else:
        if request.form.get('csrf_token') == \
                session.get('blog_modify_csrf_token'):
            title = request.form.get('title')
            slug = request.form.get('slug')
            tag = request.form.get('tag')
            post_type = request.form.get('type')
            text = request.form.get('editormd')
            url_en = request.form.get("url")
            image_url = request.form.get("image")
            template = request.form.get("template")
            content = Content.query.filter_by(id=url).first()
            content.title = title
            content.slug = slug
            content.post_type = post_type
            content.text = text
            content.url_en = url_en
            content.tag = tag
            content.image_url = image_url
            content.template = template
            if content.updata():
                return redirect(url_for("article.post", url=url))
            else:
                return "错误", 302

        else:
            return "错误", 302
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
                content = Content.query.filter(
                    Content.id == article_id).first()
                if content.delete():
                    print("ok")
            content_list = Content.query.all()
            data_list = []
            for data in content_list:
                data_list.append(data.to_json())
            return jsonify(data_list)
        return jsonify({"ok": "ok"})
# 删除文章


@admin.route("/admin/blog-set/", methods=["GET", "POST"])
# 博客设置
@login_required
def blog_set():
    if request.method == "GET":
        return render_template("blog-set.html")
    else:
        if request.get_data():
            from config.rw_json import write_json
            data = request.get_json()
            print(data)
            write_json(data)
            current_app.config["INFO"] = data
            return jsonify(data)
        else:

            data = current_app.config["INFO"]
            return jsonify(data)


@admin.route('/admin/comment/', methods=['POST', "GET", "DELETE"])
# 博客评论管理
@login_required
def blog_comment():
    if request.method == "GET":
        return render_template("blog-comment.html", **locals())
    elif request.method == "POST":
        comments = ParentComment.query.all()
        data = []
        for comment in comments:
            for c_comment in comment.children_commets:
                data.append({
                    "created": str(c_comment.created),
                    "id": c_comment.id,
                    "web_site": c_comment.web_site,
                    "text": c_comment.text,
                    "guest_email": c_comment.guest_email,
                    "guest_name": c_comment.guest_name,
                    "post_id": c_comment.post_id,
                    "uuid": c_comment.uuid,
                    "parent_id": c_comment.parent_id
                })
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
        for data in deleted_list.get("delete_list"):
            if data.get("parent_id"):
                c_comment = ChildrenCommet.query.filter(
                    ChildrenCommet.id == data.get("id")
                ).first()
                if c_comment.delete():
                    status["success"] += 1
                else:
                    status["error"] += 1
            else:
                comment = ParentComment.query.filter(
                    ParentComment.id == data.get("id")
                ).first()
                if comment.delete():
                    status["success"] += 1
                else:
                    status["error"] += 1
        comments = ParentComment.query.all()
        data = []
        for comment in comments:
            for c_comment in comment.children_commets:
                data.append({
                    "created": str(c_comment.created),
                    "id": c_comment.id,
                    "web_site": c_comment.web_site,
                    "text": c_comment.text,
                    "guest_email": c_comment.guest_email,
                    "guest_name": c_comment.guest_name,
                    "post_id": c_comment.post_id,
                    "uuid": c_comment.uuid,
                    "parent_id": c_comment.parent_id
                })
            data.append({"created": str(comment.created),
                         "id": comment.id,
                         "web_site": comment.web_site,
                         "text": comment.text,
                         "guest_email": comment.guest_email,
                         "guest_name": comment.guest_name,
                         "post_id": comment.post_id,
                         "uuid": comment.uuid})
        return jsonify({"data": data, "status": status})


@admin.route('/admin/server-info/', methods=['POST'])
# 服务器信息
@login_required
def server_info():
    data = get_server_info()
    return jsonify(data)
