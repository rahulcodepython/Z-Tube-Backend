from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from djoser.conf import settings
from . import create_username

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'username',
            settings.LOGIN_FIELD
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        user.username = create_username.create_username(validated_data['email'].split(
            '@')[0])
        user.save()
        return user
