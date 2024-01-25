from rest_framework import serializers
from . import models
from authentication import models as auth_model


class PostSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField())
    media = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = models.Post
        fields = '__all__'


class PostConfigSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.PostConfig
        exclude = ['visibleTo', 'hiddenFrom']


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    master = serializers.StringRelatedField(read_only=True)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Comment
        fields = '__all__'

    def get_uploader(self, obj):
        profile = auth_model.Profile.objects.get(user=obj.uploader)
        return {
            "name": f"{obj.uploader.first_name} {obj.uploader.last_name}",
            "image": profile.image
        }
