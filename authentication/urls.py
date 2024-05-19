from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("users/me/", views.UserView.as_view()),
    path("users/me/user/", views.UserPeekView.as_view()),
    path("users/user/<str:username>/", views.OtherUserView.as_view()),
    path("users/activation/", views.ActivateUserView.as_view()),
    path("users/resend_activation/", views.ResendActivateUserView.as_view()),
    path("users/jwt/create/", views.CreateJWTView.as_view()),
    path("users/jwt/refresh/", TokenRefreshView.as_view()),
    path("users/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/set_password/", views.ResetUserPasswordView.as_view()),
    path("users/set_email/", views.ResetUserEmailView.as_view()),
    path(
        "github/code/",
        views.GithubAuthRedirectView.as_view(),
        name="github_auth_redirect",
    ),
    path(
        "github/authenticate/",
        views.GithubAuthenticateView.as_view(),
        name="github_authenticate",
    ),
    path(
        "google/code/",
        views.GoogleAuthRedirectView.as_view(),
        name="google_auth_redirect",
    ),
    path(
        "google/authenticate/",
        views.GoogleAuthenticateView.as_view(),
        name="google_authenticate",
    ),
    # Others Actions
    path("find/username/", views.FindUsernameView.as_view()),
    path("connect/<str:username>/", views.ConnectView.as_view()),
    path("request-marchent-account/", views.RequestMarchentAccountView.as_view()),
]
