# from djoser.social.views import ProviderAuthView
from rest_framework import views, response, permissions, status
from . import serializers, models, google, jwttoken
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings

User = get_user_model()


class TestIndex(views.APIView):
    def get(self, request, format=None):
        return response.Response({"msg": "Ok! Running..."})


class GoogleAuthView(views.APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = serializers.GoogleAuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)

        validated_data = auth_serializer.validated_data
        email = google.get_user_data(validated_data)

        user = User.objects.get(email=email)

        tokens = jwttoken.get_tokens_for_user(user)

        return redirect(f"{settings.BASE_APP_URL}/auth/google/?access={
            tokens['access']}&refresh={tokens['refresh']}")


class UserDataView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            serialized_data = serializers.UserDataSerializer(request.user)

            return response.Response(serialized_data.data, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class FindUsernameView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            username = request.data['username']
            if User.objects.filter(username=username).exists():
                return response.Response({}, status=status.HTTP_403_FORBIDDEN)

            return response.Response({}, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"msg": "No user found."}, status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if profile.isLocked and request.user not in profile.Connections.all() and request.user != user:
                return response.Response({"msg": "This account is locked."}, status=status.HTTP_403_FORBIDDEN)

            serialized_data_profile = serializers.ProfileSerializer(profile)

            serialized_data_user = serializers.UserSerializer(user)

            return response.Response({
                **serialized_data_user.data,
                **serialized_data_profile.data,
                "isFriend": True if request.user in profile.Connections.all() else False,
                "self": True if request.user == user else False
            }, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username, format=None):
        try:
            if request.user.username != username:
                return response.Response({}, status=status.HTTP_403_FORBIDDEN)

            if 'email' in request.data:
                del request.data["email"]

            if 'username' in request.data and User.objects.filter(username=request.data["username"]).exists():
                del request.data["username"]

            serialized_data_user = serializers.UserSerializer(
                request.user, data=request.data, partial=True)

            serialized_data_profile = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user), data=request.data, partial=True)

            if serialized_data_user.is_valid() and serialized_data_profile.is_valid():

                serialized_data_user.save()
                serialized_data_profile.save()

                serialized_data_user_basic_data = serializers.UserDataSerializer(
                    request.user)

                return response.Response({
                    "profile": {
                        **serialized_data_profile.data,
                        **serialized_data_user.data,
                        "isFriend": False,
                        "self": True
                    },
                    "user": serialized_data_user_basic_data.data
                }, status=status.HTTP_202_ACCEPTED)

            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class ConnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user not in profile.Connections.all():
                profile.Connections.add(request.user)

            profile.followers += 1
            profile.save()

            return response.Response({"success": "You are now connected."}, status=status.HTTP_202_ACCEPTED)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user in profile.Connections.all():
                profile.Connections.remove(request.user)

            profile.followers += 1
            profile.save()

            return response.Response({"success": "You are now disconnected."}, status=status.HTTP_202_ACCEPTED)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)
