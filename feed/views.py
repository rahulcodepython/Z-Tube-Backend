from rest_framework import views, response, status, permissions
from . import models, serializers
from django.contrib.auth import get_user_model

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
                return response.Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post.save()

            postConfig = models.PostConfig.objects.create(
                id=models.Post.objects.get(id=serialized_post.data['id']), createdAt=request.data['createdAt'])

            if (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'public'):
                postConfig.isPublic = True
                postConfig.save()
            elif (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'protected'):
                postConfig.isProtected = True
                postConfig.save()
            elif (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'private'):
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
            return response.Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class ViewPostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"msg": "No such user."}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if models.PostRecord.objects.filter(user=user).exists():
                postRecord = models.PostRecord.objects.get(user=user)
                posts = postRecord.posts.all()

                postsList = []

                for post in posts:
                    serialized_post = serializers.PostSerializer(post)
                    serialized_post_config = serializers.PostConfigSerializer(
                        models.PostConfig.objects.get(id=post.id))
                    postsList.append(
                        {**serialized_post.data, **serialized_post_config.data, **{"self": True if request.user == user else False}})

                return response.Response(postsList, status=status.HTTP_200_OK)
            else:
                return response.Response({"msg": "No Post Here"},
                                         status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return response.Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
