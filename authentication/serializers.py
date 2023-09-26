from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from djoser.conf import settings

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email
        data['username'] = self.user.username
        data['image'] = self.user.image.url
        data['is_superuser'] = self.user.is_superuser
        return data


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'username',
            'image',
            settings.LOGIN_FIELD
        )
