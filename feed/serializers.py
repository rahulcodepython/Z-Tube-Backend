from rest_framework import serializers
from . import models


class CreatePostSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField())
    media = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = models.Post
        fields = '__all__'


class CreatePostConfigSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.PostConfig
        fields = '__all__'
