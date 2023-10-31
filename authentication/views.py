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


class UserDataView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            serialized_data = serializers.UserSerializer(request.user)
            return response.Response(serialized_data.data)

        except Exception as e:
            return response.Response(f"{e}")


class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"msg": "No user is found."})

            serialized_data = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user))

            if user is request.user:
                serialized_data.data['self'] = True
                return response.Response(serialized_data.data)

            serialized_data.data['self'] = False
            return response.Response(serialized_data.data)

        except Exception as e:
            return response.Response(f"{e}")

    def patch(self, request, format=None):
        try:
            if 'user' and 'email' in request.data['user']:
                del request.data["user"]["email"]

            if 'user' and 'username' in request.data['user'] and User.objects.filter(username=request.data["user"]["username"]).exists():
                del request.data["user"]["username"]

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

            return response.Response(serialized_data_profile.data)

        except Exception as e:
            return response.Response(f"{e}")
