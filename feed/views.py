from rest_framework import views, response, status, permissions
from . import models, serializers
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

POST_VISIBILITY_TYPE = [
    'public',
    'protected',
    'private'
]


class CreatePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            serialized_post = serializers.PostSerializer(
                data=request.data)

            if not serialized_post.is_valid():
                return response.Response({"error": "Your data is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post.save()

            postConfig = models.PostConfig.objects.create(
                id=models.Post.objects.get(id=serialized_post.data['id']), createdAt=request.data['createdAt'], uploader=request.user, allowComments=request.data['allowComments'])

            if request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'public':
                postConfig.isPublic = True

            elif request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'protected':
                postConfig.isProtected = True

            elif request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'private':
                postConfig.isPrivate = True

            postConfig.save()

            if models.PostRecord.objects.filter(user=request.user).exists():
                record = models.PostRecord.objects.get(user=request.user)
                record.posts.add(models.Post.objects.get(
                    id=serialized_post.data['id']))
                record.save()
            else:
                record = models.PostRecord.objects.create(user=request.user)
                record.posts.add(models.Post.objects.get(
                    id=serialized_post.data['id']))
                record.save()

            serialized_post_config = serializers.PostConfigSerializer(
                models.PostConfig.objects.get(id=postConfig))

            return response.Response({**serialized_post.data, **serialized_post_config.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class EditPostView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, postid, format=None):
        try:
            post = models.Post.objects.get(id=postid) if models.Post.objects.filter(
                id=postid).exists() else None

            if post is None:
                return response.Response({"error": "No such post."}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post = serializers.PostSerializer(instance=post, data=request.data)

            if not serialized_post.is_valid():
                return response.Response({"error": "Your data is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post.save()

            postConfig = models.PostConfig.objects.get(id=post)

            postConfig.allowComments = request.data['allowComments']

            if request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'public':
                postConfig.isPublic = True
                postConfig.isProtected = False
                postConfig.isPersonal = False
                postConfig.isHidden = False
                postConfig.isPrivate = False

            elif request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'protected':
                postConfig.isProtected = True
                postConfig.isPublic = False
                postConfig.isPersonal = False
                postConfig.isHidden = False
                postConfig.isPrivate = False

            elif request.data['visibility'] in POST_VISIBILITY_TYPE and request.data['visibility'] == 'private':
                postConfig.isPrivate = True
                postConfig.isPublic = False
                postConfig.isProtected = False
                postConfig.isPersonal = False
                postConfig.isHidden = False

            postConfig.save()

            serialized_post_config = serializers.PostConfigSerializer(
                postConfig)

            return response.Response({**serialized_post.data, **serialized_post_config.data, **{"self": True if request.user == postConfig.uploader else False}}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class ViewUserAllPostsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: object, username: object) -> object:
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"error": "No such user."}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if models.PostRecord.objects.filter(user=user).exists():
                postRecord = models.PostRecord.objects.get(user=user)
                posts = postRecord.posts.all()

                postsList = []

                for post in posts:
                    serialized_post = serializers.PostSerializer(post)
                    serialized_post_config = serializers.PostConfigSerializer(
                        models.PostConfig.objects.get(id=post.id))
                    postsList.append({
                        **serialized_post.data,
                        **serialized_post_config.data,
                        **{"self": True if request.user == user else False},
                        **{
                            "user_reaction":
                            models.PostReaction.objects.get(post=post, user=request.user).reaction if models.PostReaction.objects.filter(
                                post=post, user=request.user).exists() else None
                        }
                    })

                return response.Response(postsList, status=status.HTTP_200_OK)
            else:
                return response.Response({"error": "No Post Here"},
                                         status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class CreateCommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, postid, format=None):
        try:
            post = models.Post.objects.get(id=postid) if models.Post.objects.filter(
                id=postid).exists() else None

            if post is None:
                return response.Response({'msg': 'Invalid post id.'}, status=status.HTTP_400_BAD_REQUEST)

            postConfig = models.PostConfig.objects.get(id=post)

            if not postConfig.allowComments:
                return response.Response({'msg': "Comments are not allowed to the post"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            comment_id = f"{postid}+{uuid.uuid4()}"
            master = models.Comment.objects.get(id=request.data['master']) if 'master' in request.data and models.Comment.objects.filter(
                id=request.data['master']).exists() else None

            comment = models.Comment.objects.create(
                id=comment_id, master=master, uploader=request.user, comment=request.data['comment'], createdAt=request.data['createdAt'])

            postConfig.commentNo += 1
            postConfig.save()

            if master is None:
                if models.CommentRecord.objects.filter(post=post).exists():
                    commentRecord = models.CommentRecord.objects.get(post=post)
                    commentRecord.comments.add(comment)
                    commentRecord.save()

                else:
                    commentRecord = models.CommentRecord.objects.create(
                        post=post)
                    commentRecord.comments.add(comment)
                    commentRecord.save()

            comment_serialized = serializers.CommentSerializer(comment)

            return response.Response({
                "comment": comment_serialized.data,
                "commentNo": postConfig.commentNo
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ViewCommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, postid, format=None):
        try:
            post = models.Post.objects.get(id=postid) if models.Post.objects.filter(
                id=postid).exists() else None

            if post is None:
                return response.Response({"error": "There is no such post."}, status=status.HTTP_400_BAD_REQUEST)

            comment_record = models.CommentRecord.objects.get(
                post=post) if models.CommentRecord.objects.filter(post=post).exists() else None

            if comment_record is None:
                return response.Response([], status=status.HTTP_200_OK)

            commentList = []

            for comment in comment_record.comments.all():
                serialized = serializers.CommentSerializer(comment)
                childrens = models.Comment.objects.filter(master=comment.id)
                childList = []

                for child in childrens:
                    serialized_children = serializers.CommentSerializer(child)
                    childList.append(serialized_children.data)

                commentList.append(
                    {**serialized.data, **{"children": childList}})

            return response.Response(commentList, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class CommentEditView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, commentid, format=None):
        try:
            comment = models.Comment.objects.get(
                id=commentid) if models.Comment.objects.filter(id=commentid).exists() else None

            if comment is None:
                return response.Response({"error": "There is no such comment"}, status=status.HTTP_400_BAD_REQUEST)

            if request.data['comment'] is None:
                return response.Response({"error": "No comment is passed"}, status=status.HTTP_400_BAD_REQUEST)

            comment.comment = request.data['comment']
            comment.save()

            serialized = serializers.CommentSerializer(comment)

            return response.Response(serialized.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class AddPostReactionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, postid, reaction, format=None):
        try:
            post = models.Post.objects.get(id=postid) if models.Post.objects.filter(
                id=postid).exists() else None

            if post is None:
                return response.Response({"error": "No Such Post is there."}, status=status.HTTP_400_BAD_REQUEST)

            post_config = models.PostConfig.objects.get(id=post)

            if models.PostReaction.objects.filter(post=post, user=request.user).exists():
                reaction_record = models.PostReaction.objects.get(
                    post=post, user=request.user)
                reaction_record.reaction = reaction
            else:
                reaction_record = models.PostReaction.objects.create(
                    post=post, user=request.user)
                reaction_record.reaction = reaction
                post_config.likeNo += 1
                post_config.save()

            reaction_record.save()

            return response.Response({"likeNo": post_config.likeNo}, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, postid, reaction, format=None):
        try:
            post = models.Post.objects.get(id=postid) if models.Post.objects.filter(
                id=postid).exists() else None

            if post is None:
                return response.Response({"error": "No Such Post is there."}, status=status.HTTP_400_BAD_REQUEST)

            post_config = models.PostConfig.objects.get(id=post)

            if models.PostReaction.objects.filter(post=post, user=request.user).exists():
                post_reaction = models.PostReaction.objects.get(
                    post=post, user=request.user)
                post_reaction.delete()
                post_config.likeNo -= 1
                post_config.save()

            return response.Response({"likeNo": post_config.likeNo}, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
