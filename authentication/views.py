from djoser.social.views import ProviderAuthView
from rest_framework import permissions
from rest_framework import views, response
from . import serializers


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class BasicUserDataView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serialized_data = serializers.BasicUserDataSerializer(request.user)
        return response.Response(serialized_data.data)
