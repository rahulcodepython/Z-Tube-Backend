from rest_framework import views, response, status, permissions
from . import models, serializers
from django.contrib.auth import get_user_model

User = get_user_model()

POST_VISIBILITY_TYPE = [
    'public',
    'protected'
    'private'
]


class CreatePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            serialized_post = serializers.CreatePostSerializer(
                data=request.data)

            if not serialized_post.is_valid():
                return response.Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

            serialized_post.save()

            postConfig = models.PostConfig.objects.create(
                id=models.Post.objects.get(id=serialized_post.data['id']), master=request.user)

            if (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'public'):
                print("public")
                print(postConfig.isPublic)
                postConfig.isPublic = True
                postConfig.save()
            elif (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'protected'):
                print("public")
                print(postConfig.isProtected)
                postConfig.isProtected = True
                postConfig.save()
            elif (request.data['visibility']['type'] in POST_VISIBILITY_TYPE and request.data['visibility']['type'] == 'private'):
                print("public")
                print(postConfig.isPrivate)
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

            serialized_post_config = serializers.CreatePostConfigSerializer(
                models.PostConfig.objects.get(id=postConfig))

            return response.Response({**serialized_post.data, **serialized_post_config.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return response.Response({"msg": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
