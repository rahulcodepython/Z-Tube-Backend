from rest_framework import views, response, status, permissions
from . import models, serializers
from authentication import models as auth_models
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
import uuid
import os

User = get_user_model()

POST_VISIBILITY_TYPE = ["public", "protected", "private"]

POST_PAGINATION_DEFAULT_LIMIT = 3


class CreatePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            serialized = serializers.PostSerializer(data=request.data)

            if not serialized.is_valid():
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            serialized.save(uploader=request.user)

            post = models.Post.objects.get(id=serialized.data["id"])

            if request.data["visibility"] == "public":
                post.isPublic = True
                post.isProtected = False
                post.isPersonal = False
                post.isHidden = False
                post.isPrivate = False

            elif request.data["visibility"] == "protected":
                post.isProtected = True
                post.isPublic = False
                post.isPersonal = False
                post.isHidden = False
                post.isPrivate = False

            elif request.data["visibility"] == "private":
                post.isPrivate = True
                post.isPublic = False
                post.isProtected = False
                post.isPersonal = False
                post.isHidden = False
            else:
                post.isPublic = True
                post.isProtected = False
                post.isPersonal = False
                post.isHidden = False
                post.isPrivate = False

            post.save()

            if models.PostRecord.objects.filter(user=request.user).exists():
                record = models.PostRecord.objects.get(user=request.user)
                record.posts.add(post)
                record.save()
            else:
                record = models.PostRecord.objects.create(user=request.user)
                record.posts.add(post)
                record.save()

            serialized_post = serializers.PostSerializer(post)

            profile = auth_models.Profile.objects.get(user=request.user)
            profile.posts += 1
            profile.save()

            return response.Response(
                {
                    "content": {**serialized_post.data, "self": True},
                    "posts": profile.posts,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class EditPostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, postid, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post = serializers.PostSerializer(
                instance=post, data=request.data
            )

            if not serialized_post.is_valid():
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post.save()

            if (
                request.data["visibility"] in POST_VISIBILITY_TYPE
                and request.data["visibility"] == "public"
            ):
                post.isPublic = True
                post.isProtected = False
                post.isPersonal = False
                post.isHidden = False
                post.isPrivate = False

            elif (
                request.data["visibility"] in POST_VISIBILITY_TYPE
                and request.data["visibility"] == "protected"
            ):
                post.isProtected = True
                post.isPublic = False
                post.isPersonal = False
                post.isHidden = False
                post.isPrivate = False

            elif (
                request.data["visibility"] in POST_VISIBILITY_TYPE
                and request.data["visibility"] == "private"
            ):
                post.isPrivate = True
                post.isPublic = False
                post.isProtected = False
                post.isPersonal = False
                post.isHidden = False

            post.save()

            serialized_post = serializers.PostSerializer(post)

            return response.Response(
                {**serialized_post.data, "self": True}, status=status.HTTP_201_CREATED
            )

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, postid, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if post.uploader != request.user:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            post.delete()

            profile = auth_models.Profile.objects.get(user=request.user)
            profile.posts -= 1
            profile.save()

            return response.Response(
                {"posts": profile.posts}, status=status.HTTP_200_OK
            )

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class ViewUserAllPostsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            page = request.GET.get("page")
            page = 1 if page is None else page

            user = (
                User.objects.get(username=username)
                if User.objects.filter(username=username).exists()
                else None
            )

            if user is None:
                return response.Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

            profile = auth_models.Profile.objects.get(user=user)

            if (
                profile.isLocked
                and request.user not in profile.Connections.all()
                and request.user != user
            ):
                return response.Response([], status=status.HTTP_204_NO_CONTENT)

            if models.PostRecord.objects.filter(user=user).exists():
                postRecord = models.PostRecord.objects.get(user=user)
                posts = postRecord.posts.all().order_by("-timestamp")

                postsList: list = []
                serializedPostsList: list = []

                for post in posts:
                    if post.isPublic:
                        postsList.append(post)

                    elif post.isPersonal and request.user == user:
                        postsList.append(post)

                    elif post.isProtected:
                        profile = auth_models.Profile.objects.get(user=user)
                        if request.user in profile.Connections.all():
                            postsList.append(post)

                    elif post.isHidden:
                        if request.user not in post.hiddenFrom.all():
                            postsList.append(post)

                    elif post.isPrivate:
                        if request.user in post.visibleTo.all():
                            postsList.append(post)

                paginator = Paginator(postsList, POST_PAGINATION_DEFAULT_LIMIT)
                paginated = paginator.page(page)

                for post in paginated.object_list:
                    serialized_post = serializers.PostSerializer(post)
                    serializedPostsList.append(
                        {
                            **serialized_post.data,
                            "self": True if request.user == user else False,
                            "user_reaction": (
                                models.PostReaction.objects.get(
                                    post=post, user=request.user
                                ).reaction
                                if models.PostReaction.objects.filter(
                                    post=post, user=request.user
                                ).exists()
                                else None
                            ),
                        }
                    )

                url = f"{os.environ.get('BASE_API_URL')}/feed/posts/{username}/"

                return response.Response(
                    {
                        "count": paginator.count,
                        "next": (
                            f"{url}?page={paginated.next_page_number()}"
                            if paginated.has_next()
                            else None
                        ),
                        "previous": (
                            f"{url}?page={paginated.previous_page_number()}"
                            if paginated.has_previous()
                            else None
                        ),
                        "results": serializedPostsList,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return response.Response([], status=status.HTTP_204_NO_CONTENT)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class CreateCommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, postid, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if not post.allowComments:
                return response.Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)

            comment_id = f"{postid}+{uuid.uuid4()}"
            master = (
                models.Comment.objects.get(id=request.data["master"])
                if "master" in request.data
                and models.Comment.objects.filter(id=request.data["master"]).exists()
                else None
            )

            comment = models.Comment.objects.create(
                id=comment_id,
                master=master,
                uploader=request.user,
                post=post,
                comment=request.data["comment"],
                createdAt=request.data["createdAt"],
            )

            post.commentNo += 1
            post.save()

            if master is None:
                if models.CommentRecord.objects.filter(post=post).exists():
                    commentRecord = models.CommentRecord.objects.get(post=post)
                    commentRecord.comments.add(comment)
                    commentRecord.save()

                else:
                    commentRecord = models.CommentRecord.objects.create(post=post)
                    commentRecord.comments.add(comment)
                    commentRecord.save()

            comment_serialized = serializers.CommentSerializer(comment)

            return response.Response(
                {
                    "comment": {**comment_serialized.data, "self": True},
                    "commentNo": post.commentNo,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception:
            return response.Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ViewCommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, postid, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            comment_record = (
                models.CommentRecord.objects.get(post=post)
                if models.CommentRecord.objects.filter(post=post).exists()
                else None
            )

            if comment_record is None:
                return response.Response([], status=status.HTTP_200_OK)

            commentList = []

            for comment in comment_record.comments.all().order_by("-timestamp"):
                serialized = serializers.CommentSerializer(comment)
                childrens = models.Comment.objects.filter(master=comment.id)
                childList = []

                for child in childrens:
                    serialized_children = serializers.CommentSerializer(child)
                    childList.append(
                        {
                            **serialized_children.data,
                            "self": True if request.user == child.uploader else False,
                        }
                    )

                commentList.append(
                    {
                        **serialized.data,
                        "self": True if request.user == comment.uploader else False,
                        "children": childList,
                    }
                )

            return response.Response(commentList, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class CommentEditView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, commentid, format=None):
        try:
            comment = (
                models.Comment.objects.get(id=commentid)
                if models.Comment.objects.filter(id=commentid).exists()
                else None
            )

            if comment is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if request.data["comment"] is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            comment.comment = request.data["comment"]
            comment.save()

            serialized = serializers.CommentSerializer(comment)

            return response.Response(
                {**serialized.data, "self": True}, status=status.HTTP_200_OK
            )
        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, commentid, format=None):
        try:
            comment = (
                models.Comment.objects.get(id=commentid)
                if models.Comment.objects.filter(id=commentid).exists()
                else None
            )

            if comment is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if comment.uploader != request.user:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            comment.delete()

            comment.post.commentNo -= 1
            comment.post.save()

            return response.Response(
                {"commentNo": comment.post.commentNo}, status=status.HTTP_200_OK
            )

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class AddPostReactionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, postid, reaction, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if models.PostReaction.objects.filter(
                post=post, user=request.user
            ).exists():
                reaction_record = models.PostReaction.objects.get(
                    post=post, user=request.user
                )
                reaction_record.reaction = reaction
            else:
                reaction_record = models.PostReaction.objects.create(
                    post=post, user=request.user
                )
                reaction_record.reaction = reaction
                post.likeNo += 1
                post.save()

            reaction_record.save()

            return response.Response({"likeNo": post.likeNo}, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, postid, reaction, format=None):
        try:
            post = (
                models.Post.objects.get(id=postid)
                if models.Post.objects.filter(id=postid).exists()
                else None
            )

            if post is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            if models.PostReaction.objects.filter(
                post=post, user=request.user
            ).exists():
                post_reaction = models.PostReaction.objects.get(
                    post=post, user=request.user
                )
                post_reaction.delete()
                post.likeNo -= 1
                post.save()

            return response.Response({"likeNo": post.likeNo}, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)
