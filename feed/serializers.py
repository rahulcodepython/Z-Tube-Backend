from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    tags = serializers.ListField(child=serializers.CharField())
    media = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = models.Post
        fields = '__all__'


class PostConfigSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField(read_only=True)
    master = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.PostConfig
        fields = '__all__'
