from rest_framework import views, response
from . import models, serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreatePostView(views.APIView):
    def post(self, request, format=None):
        try:
            user = User.objects.get(email="rd21102004@gmail.com")

            post = models.Post.objects.create(
                caption=request.data['caption'], tags=request.data['tags'], media=request.data['media'])
            postConfig = models.PostConfig.objects.create(id=post, master=user)

            if models.PostRecord.objects.filter(user=user).exists():
                record = models.PostRecord.objects.get(user=user)
                record.posts.add(post)
                record.save()
            else:
                record = models.PostRecord.objects.create(user=user)
                record.posts.add(post)
                record.save()

            serialized_post = serializers.CreatePostSerializer(
                models.Post.objects.get(id=post))
            serialized_post_config = serializers.CreatePostConfigSerializer(
                models.PostConfig.objects.get(id=postConfig))
            data = {**serialized_post.data, **serialized_post_config.data}

            return response.Response({"msg": "Ok", "data": data})

        except Exception as e:
            return response.Response({"msg": f"{e}"}, status=400)
