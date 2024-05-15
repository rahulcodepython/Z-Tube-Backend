from rest_framework import serializers
from . import models
from authentication import serializers as auth_serializers


class PostSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    createdAt = serializers.CharField(required=False)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Post
        fields = [
            "id",
            "caption",
            "tags",
            "media",
            "uploader",
            "createdAt",
            "isPublic",
            "isProtected",
            "isPersonal",
            "isHidden",
            "isPrivate",
            "likeNo",
            "viewsNo",
            "share",
            "allowComments",
            "commentNo",
        ]

    def get_uploader(self, obj):
        return auth_serializers.UserPeekSerializer(obj.uploader).data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    master = serializers.StringRelatedField(read_only=True)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Comment
        exclude = ["post", "timestamp"]

    def get_uploader(self, obj):
        return auth_serializers.UserPeekSerializer(obj.uploader).data
