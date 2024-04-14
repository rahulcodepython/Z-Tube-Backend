from rest_framework import serializers
from . import models
from authentication import models as auth_model


class PostSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField())
    media = serializers.ListField(child=serializers.CharField())
    createdAt = serializers.CharField(required=False)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Post
        exclude = ['visibleTo', 'hiddenFrom', 'timestamp']

    def get_uploader(self, obj):
        profile = auth_model.Profile.objects.get(user=obj.uploader)
        return {
            "name": f"{obj.uploader.first_name} {obj.uploader.last_name}",
            "username": obj.uploader.username,
            "image": profile.image
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    master = serializers.StringRelatedField(read_only=True)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Comment
        exclude = ['post', 'timestamp']

    def get_uploader(self, obj):
        profile = auth_model.Profile.objects.get(user=obj.uploader)
        return {
            "name": f"{obj.uploader.first_name} {obj.uploader.last_name}",
            "username": obj.uploader.username,
            "image": profile.image
        }
