from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    re_path(r'^auth/o/(?P<provider>\S+)/$', views.CustomProviderAuthView.as_view(), name='google-auth-provider'),
]