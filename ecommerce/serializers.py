from rest_framework import serializers
from . import models
from authentication import serializers as auth_serializers


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Product
        fields = [
            "name",
            "description",
            "price",
            "offer",
            "category",
            "subcategory",
            "images",
            "availibile_quantity",
            "quanity",
            "availibility",
        ]


class GetAllMyProductsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "price",
            "offer",
            "category",
            "subcategory",
            "image",
            "availibility",
            "uploader",
            "rating",
        ]

    def get_image(self, obj):
        return obj.images[0]
