from djoser.social.views import ProviderAuthView
from rest_framework import views, response, permissions, status
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
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)


class SelfProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            serialized_data = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user), context={'request': request})

            return response.Response(serialized_data.data)

        except Exception as e:
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        try:
            if 'user' and 'email' in request.data['user']:
                del request.data["user"]["email"]

            if 'user' and 'username' in request.data['user'] and User.objects.filter(username=request.data["user"]["username"]).exists():
                del request.data["user"]["username"]

            serialized_data_user = serializers.UserSerializer(
                request.user, data=request.data['user'], partial=True)
            serialized_data_profile = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user), context={'request': request}, data=request.data, partial=True)

            if not serialized_data_user.is_valid():
                return response.Response('error', status=status.HTTP_400_BAD_REQUEST)

            if not serialized_data_profile.is_valid():
                return response.Response('error', status=status.HTTP_400_BAD_REQUEST)

            serialized_data_user.save()
            serialized_data_profile.save()

            return response.Response(serialized_data_profile.data)

        except Exception as e:
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response("No user found", status=status.HTTP_400_BAD_REQUEST)

            serialized_data = serializers.ProfileSerializer(
                models.Profile.objects.get(user=user), context={'request': request})

            return response.Response(serialized_data.data)

        except Exception as e:
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)


class ConnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response("No user found", status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user not in profile.Connections.all():
                profile.Connections.add(request.user)

            return response.Response("You are now connected.", status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response("No user found", status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user in profile.Connections.all():
                profile.Connections.remove(request.user)

            return response.Response("You are now disconnected.", status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
