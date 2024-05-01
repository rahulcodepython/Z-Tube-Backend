from rest_framework import views, response, status, permissions
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . import serializers, email, models
from django.conf import settings
import requests
import random

User = get_user_model()


def create_uid() -> int:
    return random.randint(1000, 9999)


def create_token() -> int:
    return random.randint(1000, 9999)


class TestIndex(views.APIView):
    def get(self, request):
        return response.Response({"msg": "Ok! Running..."})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def check_email_exists(entered_email):
    return User.objects.filter(email=entered_email).exists()


def check_authenticated_user(user):
    return user.is_authenticated


def check_user_active(entered_email: str) -> bool:
    user = User.objects.get(email=entered_email)
    return user.is_active


def response_unauthorized_access():
    return response.Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)


def response_bad_request(e):
    return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def response_ok(e):
    return response.Response({"success": str(e)}, status=status.HTTP_200_OK)


class UserView(views.APIView):
    def create_uid(self) -> int:
        uid: int = create_uid()
        if models.ActivationCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self) -> int:
        token: int = create_token()
        if models.ActivationCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    @staticmethod
    def generate_unique_username(given_email):
        return given_email.split('@')[0]

    def get(self, request):
        try:
            return response.Response({
                **serializers.UserSerializer(request.user).data,
                "self": True
            },status=status.HTTP_200_OK) if check_authenticated_user(request.user) else response.Response({
                "error": "You are not authenticated yet."
            },status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return response_bad_request(e)

    def post(self, request):
        try:
            if check_email_exists(request.data["email"]):
                if not check_user_active(request.data["email"]):
                    return response.Response({
                        "error": "You have already registered. But not verified you email yet. Please verify it first."
                    }, status=status.HTTP_406_NOT_ACCEPTABLE)

                return response.Response({"error": "You have already registered."},
                                         status=status.HTTP_406_NOT_ACCEPTABLE)

            serialized_data = serializers.UserCreateSerializer(
                data={**request.data, "username": self.generate_unique_username(request.data["email"])})

            if not serialized_data.is_valid():
                return response.Response({"error": str(serialized_data.errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)

            user = serialized_data.save()

            activation_code = models.ActivationCode.objects.create(
                user=user, uid=self.create_uid(), token=self.create_token()
            )
            email.activation_email(uid=activation_code.uid, token=activation_code.token, email=user.email,
                                   username=user.username)

            return response.Response({"success": "Your account has been creates. At First verify it."},
                                     status=status.HTTP_201_CREATED)

        except Exception as e:
            return response_bad_request(e)

    def patch(self, request):
        try:
            if not check_authenticated_user(request.user):
                return response_unauthorized_access()

            serialized_data = serializers.UserUpdateSerializer(
                request.user, data=request.data, partial=True
            )

            if not serialized_data.is_valid():
                return response.Response({"error": str(serialized_data.errors)}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serialized_data.save()

            return response.Response({"success": "Your data is updated."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response_bad_request(e)

    def delete(self, request):
        try:
            if not check_authenticated_user(request.user):
                return response_unauthorized_access()

            request.user.delete()
            return response.Response({"success": "Your account is deleted."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response_bad_request(e)


class OtherUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        try:
            if not User.objects.filter(username=username).exists():
                return response_bad_request("No such user found.")

            return response.Response({
                **serializers.UserSerializer(User.objects.get(username=username)).data,
                "self": False
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(e)


class ActivateUserView(views.APIView):
    def post(self, request):
        try:
            uid = request.data["uid"]
            token = request.data["token"]
            user = (
                models.ActivationCode.objects.filter(uid=uid, token=token)[0].user
                if models.ActivationCode.objects.filter(uid=uid, token=token).exists()
                else None
            )

            if user is None:
                return response_bad_request("You have entered wrong code. Try again.")

            user.is_active = True
            user.save()
            models.ActivationCode.objects.filter(uid=uid, token=token)[0].delete()

            return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(e)


class ResendActivateUserView(views.APIView):
    def create_uid(self):
        uid = create_uid()
        if models.ActivationCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = create_token()
        if models.ActivationCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def post(self, request):
        try:
            user_email = request.data["email"]

            if not check_email_exists(user_email):
                return response_bad_request("No such user is there. Try again.")

            user = User.objects.get(email=user_email)

            if check_user_active(user_email):
                return response.Response({"error": "You are already verified."}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if models.ActivationCode.objects.filter(user=user).exists():
                models.ActivationCode.objects.get(user=user).delete()

            activation_code = models.ActivationCode.objects.create(
                user=user, uid=self.create_uid(), token=self.create_token()
            )

            email.activation_email(uid=activation_code.uid, token=activation_code.token, email=user.email,
                                   username=user.username)

            return response_ok("Activation link has been sent to your email.")

        except Exception as e:
            return response_bad_request(e)


class CreateJWTView(views.APIView):
    def post(self, request):
        try:
            given_email = request.data["email"]
            password = request.data["password"]

            if not User.objects.filter(email=given_email).exists():
                return response_bad_request("No such user is there. Try again.")

            user = authenticate(username=User.objects.get(email=given_email).username, password=password)

            if user is None:
                return response_bad_request("No such user is there. Try again.")

            if not user.is_active:
                return response.Response({"error": "You are not verified yet. Verify first."},
                                         status=status.HTTP_406_NOT_ACCEPTABLE)

            return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(e)


class ResetUserPasswordView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def create_uid(self):
        uid = create_uid()
        if models.ResetPasswordCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = create_token()
        if models.ResetPasswordCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def get(self, request):
        try:
            if models.ResetPasswordCode.objects.filter(user=request.user).exists():
                models.ResetPasswordCode.objects.get(user=request.user).delete()

            reset_password_code = models.ResetPasswordCode.objects.create(
                user=request.user, uid=self.create_uid(), token=self.create_token()
            )
            email.reset_email_confirmation(uid=reset_password_code.uid, token=reset_password_code.token,
                                           email=request.user.email, username=request.user.username)

            return response_ok("Reset Password link is sent to your mail.")

        except Exception as e:
            return response_bad_request(e)

    def post(self, request):
        try:
            new_password = request.data["new_password"]
            current_password = request.data["current_password"]
            uid = request.data["uid"]
            token = request.data["token"]

            if not models.ResetPasswordCode.objects.filter(uid=uid, token=token).exists():
                return response.Response({"error": "You have entered wrong code. Try again."},
                                         status=status.HTTP_406_NOT_ACCEPTABLE)

            reset_password_code = models.ResetPasswordCode.objects.filter(uid=uid, token=token)[0]

            if reset_password_code.user != request.user:
                return response_unauthorized_access()

            user = request.user

            if not user.check_password(current_password):
                return response_bad_request("Your current password is not correct. Try again.")

            user.set_password(new_password)
            user.save()

            reset_password_code.delete()

            return response_ok("Successfully changed the password")

        except Exception as e:
            return response_bad_request(e)


class ResetUserEmailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def create_uid(self):
        uid = create_uid()
        if models.ResetEmailCode.objects.filter(uid=uid).exists():
            self.create_uid()
        return uid

    def create_token(self):
        token = create_token()
        if models.ResetEmailCode.objects.filter(token=token).exists():
            self.create_token()
        return token

    def post(self, request):
        try:
            new_email = request.data["email"]

            if models.ResetEmailCode.objects.filter(user=request.user).exists():
                models.ResetEmailCode.objects.get(user=request.user).delete()

            reset_email_code = models.ResetEmailCode.objects.create(
                user=request.user, uid=self.create_uid(), token=self.create_token(), email=new_email
            )
            email.reset_email_confirmation(uid=reset_email_code.uid, token=reset_email_code.token,
                                           email=new_email, username=request.user.username)

            return response_ok("Reset Email link is sent to your email.")

        except Exception as e:
            return response_bad_request(e)


class UpdateEmailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            uid = request.data["uid"]
            token = request.data["token"]

            if not models.ResetEmailCode.objects.filter(uid=uid, token=token).exists():
                return response.Response({"error": "You have entered wrong code. Try again."},
                                         status=status.HTTP_406_NOT_ACCEPTABLE)

            reset_email_code = models.ResetEmailCode.objects.filter(uid=uid, token=token)[0]

            if reset_email_code.user != request.user:
                return response_unauthorized_access()

            user = request.user
            user.email = reset_email_code.email
            user.save()

            reset_email_code.delete()

            return response_ok("Successfully email is updated.")

        except Exception as e:
            return response_bad_request(e)


class GithubAuthRedirectView(views.APIView):
    def get(self, request):
        return response.Response({
            "url": f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}&scope=user"
        }, status=status.HTTP_200_OK)


class GithubAuthenticateView(views.APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")

            if not code:
                return response_bad_request("Authorization code not provided")

            data = {
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            }

            response_github = requests.post(
                "https://github.com/login/oauth/access_token",
                data=data,
                headers={"Accept": "application/json"},
            )
            access_token = response_github.json().get("access_token")

            if not access_token:
                return response_bad_request("Authorization Failed.")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {access_token}"},
            ).json()

            github_username = user_data.get("login")
            if User.objects.filter(username=github_username).exists():
                user = User.objects.get(username=github_username)
                return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

            github_email = user_data.get("email") if user_data.get("email") else None
            first_name = user_data.get("name").split()[0]
            last_name = ''.join(user_data.get("name").split()[1:])
            password = user_data.get("node_id")
            image = user_data.get("avatar_url")
            bio = user_data.get("bio")

            user = User.objects.create_user(
                email=github_email,
                username=github_username,
                first_name=first_name,
                last_name=last_name,
                image=image,
                bio=bio,
                method='Github',
                is_active=True
            )
            user.set_password(password)
            user.save()

            return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(e)


class GoogleAuthRedirectView(views.APIView):
    def get(self, request):
        return response.Response({
            "url": f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=email%20profile&response_type=code"
        }, status=status.HTTP_200_OK)


class GoogleAuthenticateView(views.APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")

            if not code:
                return response_bad_request("Authorization code not provided")

            data = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }

            response_google = requests.post("https://oauth2.googleapis.com/token", data=data)
            access_token = response_google.json().get("access_token")

            if not access_token:
                return response_bad_request("Authorization Failed.")

            user_data = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            ).json()

            google_email = user_data.get("email")

            if User.objects.filter(email=google_email).exists():
                user = User.objects.get(email=google_email)
                return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

            google_username = google_email.split("@")[0]
            first_name = user_data.get("given_name")
            last_name = user_data.get("family_name")
            password = user_data.get("id")
            image = user_data.get("picture")

            user = User.objects.create_user(
                email=google_email,
                username=google_username,
                first_name=first_name,
                last_name=last_name,
                image=image,
                method='Google',
                is_active=True
            )
            user.set_password(password)
            user.save()

            return response.Response(get_tokens_for_user(user), status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserPeekView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            return response.Response(serializers.UserPeekSerializer(request.user).data, status=status.HTTP_200_OK)

        except Exception as e:
            return response_bad_request(e)


class FindUsernameView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            return response.Response({}, status=status.HTTP_403_FORBIDDEN) if User.objects.filter(
                username=request.data['username']).exists() else response.Response({}, status=status.HTTP_200_OK)

        except Exception:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)


class ConnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response_bad_request("No such user is found")

            if request.user not in user.Connections.all():
                user.Connections.add(request.user)

            user.followers += 1
            user.save()

            return response.Response({"success": "You are now connected."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response_bad_request(e)

    def delete(self, request, username, format=None):
        try:
            user = User.objects.get(username=username) if User.objects.filter(
                username=username).exists() else None

            if user is None:
                return response_bad_request("No such user is found")

            if request.user not in user.Connections.all():
                user.Connections.add(request.user)

            user.followers -= 1
            user.save()

            return response.Response({"success": "You are now disconnected."}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return response_bad_request(e)
