from django.urls import path
from . import views

urlpatterns = [
    path('createpost/', views.CreatePostView.as_view()),
    path('posts/', views.ViewPostView.as_view()),
]
