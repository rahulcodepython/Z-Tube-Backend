from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('dj/', include('djoser.urls')),
    path('token/', include('djoser.urls.jwt')),
    path('me/', views.UserDataView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    re_path(r'^social/o/(?P<provider>\S+)/$',
            views.CustomProviderAuthView.as_view(), name='google-auth-provider'),
]
