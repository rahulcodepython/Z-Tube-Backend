from django.urls import path
from . import views

urlpatterns = [
    path('createpost/', views.CreatePostView.as_view()),
    path('posts/<str:username>/', views.ViewPostView.as_view()),
]
