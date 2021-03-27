from flask_restplus import Namespace, Resource, marshal, fields, marshal_with
from flask import jsonify, request, current_app
from models.Content import Article
from models.Commet import ParentComment, ChildrenCommet

api = Namespace("comment", description="评论数据接口")


@api.route("/")
class Comment(Resource):

    def get(self):
        comments = ParentComment.query.filter_by(
            post_id=request.args.get("postId")).all()
        comment_list = []
        print(request.args.get("postId"))
        for comment in comments:
            children_list = []
            for c_comment in comment.children_commets:
                children_list.append(
                    {"guest_name": c_comment.guest_name,
                     "created": c_comment.created,
                     "hash_email": c_comment.hash_email,
                     "text": c_comment.text,
                     'id': c_comment.id,
                     "parentId": c_comment.parent_id,
                     'uuid': c_comment.uuid
                     }
                )
            comment_list.append({"guest_name": comment.guest_name,
                                 "created": comment.created,
                                 "hash_email": comment.hash_email,
                                 "text": comment.text,
                                 "id": comment.id,
                                 'uuid': comment.uuid,
                                 "children_comment": children_list})
        return jsonify({'data': comment_list})

    def post(self):
        data = request.get_json()
        if data.get("type") == "parent":
            p_comment = ParentComment(guest_email=data.get("guestEmail"),
                                      guest_name=data.get("guestName"),
                                      web_site=data.get("webSite"),
                                      text=data.get("text"),
                                      post_id=data.get("postId"))
            if p_comment.save():
                comments = ParentComment.query.filter_by(
                    post_id=data.get("postId")).all()
                comment_list = []
                for comment in comments:
                    children_list = []
                    for c_comment in comment.children_commets:
                        children_list.append(
                            {"guest_name": c_comment.guest_name,
                                "created": c_comment.created,
                                "hash_email": c_comment.hash_email,
                                "text": c_comment.text,
                                'id': c_comment.id,
                                'uuid': c_comment.uuid
                             }
                        )
                    comment_list.append({"guest_name": comment.guest_name,
                                         "created": comment.created,
                                         "hash_email": comment.hash_email,
                                         "text": comment.text,
                                         "id": comment.id,
                                         'uuid': comment.uuid,
                                         "children_comment": children_list})
                current_app.logger.info("父级评论成功")
                return jsonify({'data': comment_list})
            else:
                current_app.logger.info("父级评论失败")
                return jsonify("提交评论错误")
        elif data.get("type") == "children":
            c_comment = ChildrenCommet(guest_email=data.get("guestEmail"),
                                       guest_name=data.get("guestName"),
                                       web_site=data.get("webSite"),
                                       text=data.get("text"),
                                       post_id=data.get("postId"),
                                       parent_id=data.get("parentId"))
            if c_comment.save():
                comments = ParentComment.query.filter_by(
                    post_id=data.get("postId")).all()
                comment_list = []
                for comment in comments:
                    children_list = []
                    for c_comment in comment.children_commets:
                        children_list.append(
                            {"guest_name": c_comment.guest_name,
                                "created": c_comment.created,
                                "hash_email": c_comment.hash_email,
                                "text": c_comment.text,
                                'id': c_comment.id,
                                'uuid': c_comment.uuid
                             }
                        )
                    comment_list.append({"guest_name": comment.guest_name,
                                         "created": comment.created,
                                         "hash_email": comment.hash_email,
                                         "text": comment.text,
                                         "id": comment.id,
                                         'uuid': comment.uuid,
                                         "children_comment": children_list})
                current_app.logger.info("子级评论成功")
                return jsonify({'data': comment_list})
        else:
            current_app.logger.info("评论类型错误")
            return jsonify({"error": "评论类型错误"})


@api.route("/admin/")
class Comment(Resource):
    def get(self):
        comments = ParentComment.query.all()
        comment_list = []
        for comment in comments:
            children_list = []
            for c_comment in comment.children_commets:
                children_list.append(
                    {"guestName": c_comment.guest_name,
                     "created": c_comment.created,
                     "guestEmail": c_comment.guest_email,
                     "text": c_comment.text,
                     'id': c_comment.id,
                     'webSite': c_comment.web_site
                     }
                )
            comment_list.append({"guestName": comment.guest_name,
                                 "created": comment.created,
                                 "guestEmail": comment.guest_email,
                                 "text": comment.text,
                                 "id": comment.id,
                                 'webSite': comment.web_site,
                                 'postId':comment.post_id,
                                 "childrenComment": children_list})
        return jsonify({'data': {'comment': comment_list}})

    def delete(self):
        print(api.payload)
        return 'aa'