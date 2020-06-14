from flask_restplus import Namespace, Resource
from flask import jsonify, request
from api.v1.auth import auth
from models.Content import Content

api = Namespace("article", description="文章数据接口")


@api.route("/")
class Article(Resource):
    def get(self):
        id = request.args.get("id")
        content = Content.query.filter(Content.id == id).first_or_404()
        return jsonify({"data": {
            "article": content.to_json()
        }})

    @auth.login_required
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

        content = Content(title=title, slug=slug, user_id=user_id,
                          post_type=post_type, url_en=url_en, tag=tag,
                          image_url=image_url,
                          text=text, template=template, like_count=like_count,
                          views=views,
                          )
        if content.save():
            return {"ok": "ok"}
        else:
            return {"error": "error"}

        return jsonify(views)

    @auth.login_required
    def put(self, post):
        content = Content.query.filter(Content.id == post).first_or_404()
        data = api.payload["data"]["article"]
        content.title = data.get("title")
        content.slug = data.get("slug")
        content.user_id = data.get("user_id")
        content.post_type = data.get("post_type")
        content.url_en = data.get("url_en")
        content.tag = data.get("tag")
        content.image_url = data.get("image_url")
        content.text = data.get("text")
        content.template = data.get("template")
        content.like_count = data.get("like_count")
        content.views = data.get("views")
        if content.updata():
            return {
                "code": 201,
                "message": "success"
            }
        else:
            return {
                "code": 401,
                "message": "error"
            }

    @auth.login_required
    def delete(self, post):
        content = Content.query.filter(Content.id == post).first_or_404()
        if content.delete():
            return {
                "code": 201,
                "message": "success"
            }
        else:
            return {
                "code": 401,
                "message": "error"
            }
        # return {"put": "ok"}

# class Post():
#     def post(self, post):
#         return jsonify(api.payload)
