from django.urls import path, include
from . import views

urlpatterns = [
    path('dj/', include('djoser.urls')),
    path('token/', include('djoser.urls.jwt')),
    path('google/', views.GoogleAuthView.as_view()),
    path('me/', views.UserDataView.as_view()),
    path('find/username/', views.FindUsernameView.as_view()),
    path('profile/<str:username>/', views.ProfileView.as_view()),
    path('connect/<str:username>/', views.ConnectView.as_view()),
]
