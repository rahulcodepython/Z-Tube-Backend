from django.urls import path
from . import views

urlpatterns = [
    path('createpost/', views.CreatePostView.as_view()),
    path('posts/<str:username>/', views.ViewUserAllPostsView.as_view()),
    path('createcomment/<str:postid>/', views.CreateCommentView.as_view()),
    path('viewcomment/<str:postid>/', views.ViewCommentView.as_view()),
    path('editcomment/<str:commentid>/', views.CommentEditView.as_view()),
    path('postreaction/<str:postid>/<str:reaction>/',
         views.AddPostReactionView.as_view()),
]
