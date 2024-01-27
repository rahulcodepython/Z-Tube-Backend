from djoser.social.views import ProviderAuthView
from rest_framework import views, response, permissions, status
from . import serializers, models
from django.contrib.auth import get_user_model


User = get_user_model()


class TestIndex(views.APIView):
    def get(self, request, format=None):
        return response.Response({"msg": "Ok! Running..."})


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class UserDataView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            serialized_data = serializers.UserDataSerializer(request.user)

            return response.Response(serialized_data.data, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class FindUsernameView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            username = request.data['username']
            if User.objects.filter(username=username).exists():
                return response.Response({"error": "This username is already taken."}, status=status.HTTP_403_FORBIDDEN)

            return response.Response({}, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"error": "No user found."}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data_profile = serializers.ProfileSerializer(
                models.Profile.objects.get(user=user))

            serialized_data_user = serializers.UserSerializer(user)

            serialized_data_profileconfig = serializers.ProfileConfigSerializer(
                models.ProfileConfig.objects.get(user=user))

            return response.Response(
                {
                    **serialized_data_user.data,
                    **serialized_data_profile.data,
                    **serialized_data_profileconfig.data,
                    **{
                        "isFriend": True if request.user in models.Profile.objects.get(
                            user=user).Connections.all() else False,
                        "self": True if request.user == user else False
                    }
                },
                status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        try:
            if 'email' in request.data:
                del request.data["email"]

            if 'username' in request.data and User.objects.filter(username=request.data["username"]).exists():
                del request.data["username"]

            serialized_data_user = serializers.UserSerializer(
                request.user, data=request.data, partial=True)

            serialized_data_profile = serializers.ProfileSerializer(
                models.Profile.objects.get(user=request.user), data=request.data, partial=True)

            serialized_data_profileconfig = serializers.ProfileConfigSerializer(
                models.ProfileConfig.objects.get(user=request.user), data=request.data, partial=True)

            if serialized_data_user.is_valid() and serialized_data_profile.is_valid() and serialized_data_profileconfig.is_valid():

                serialized_data_user.save()
                serialized_data_profile.save()
                serialized_data_profileconfig.save()

                serialized_data_user_basic_data = serializers.UserDataSerializer(
                    request.user)

                return response.Response({
                    "profile": {
                        **serialized_data_profile.data,
                        **serialized_data_user.data,
                        **serialized_data_profileconfig.data,
                        **{
                            "isFriend": False,
                            "self": True
                        }
                    },
                    "user": serialized_data_user_basic_data.data
                }, status=status.HTTP_202_ACCEPTED)

            return response.Response({"error": "Data is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class ConnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"error": "No user found"}, status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user not in profile.Connections.all():
                profile.Connections.add(request.user)

            return response.Response({"msg": "You are now connected."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response.Response({"error": "No user found"}, status=status.HTTP_400_BAD_REQUEST)

            profile = models.Profile.objects.get(user=user)

            if request.user in profile.Connections.all():
                profile.Connections.remove(request.user)

            return response.Response({"msg": "You are now disconnected."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response.Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
