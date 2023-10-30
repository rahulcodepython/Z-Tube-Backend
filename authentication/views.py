from djoser.social.views import ProviderAuthView
from rest_framework import permissions
from rest_framework import views, response
from . import serializers, models
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class BasicUserDataView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serialized_data = serializers.BasicUserDataSerializer(request.user)
        return response.Response(serialized_data.data)


class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serialized_data = serializers.ProfileSerializer(
            models.Profile.objects.get(user=request.user))
        return response.Response(serialized_data.data)

    def patch(self, request, format=None):
        try:
            if 'user' and 'email' in request.data['user']:
                del request.data["user"]["email"]

            serialized_data_user = serializers.UserSerializer(
                request.user, data=request.data['user'], partial=True)
            serialized_data_profile = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user), data=request.data, partial=True)

            if not serialized_data_user.is_valid():
                return response.Response('error')

            if not serialized_data_profile.is_valid():
                return response.Response('error')

            serialized_data_user.save()
            serialized_data_profile.save()

            if 'user' and 'username' in request.data['user']:
                user = User.objects.get(email=request.user.email)
                user.username = request.data['user']['username']
                user.save()

            return response.Response(serialized_data_profile.data)

        except Exception as e:
            return response.Response(f"{e}")
