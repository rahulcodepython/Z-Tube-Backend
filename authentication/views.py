from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.social.views import ProviderAuthView
from . import serializers


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
