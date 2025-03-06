from django.urls import path
from posts import views

urlpatterns = [
    path("api/", views.PostListCreateAPIView.as_view(), name='post_cr'),
    path("api/<int:post_id>/", views.PostDetailAPIView.as_view(), name="post_ud"),
    path("api/like/<int:post_id>/", views.PostLikeAPIView.as_view(), name="post_like"),
    path("api/comment/<int:post_id>/", views.CommentCreateAPIView.as_view(), name="comment_c"),
    path("api/comment/detail/<int:comment_id>/", views.CommentDetailAPIView.as_view(), name="comment_ud"),
    path("api/comment/reply/<int:post_id>/<int:parent_id>/", views.ReplyCreateAPIView.as_view(), name="reply_c"),
    path("api/comment/like/<int:comment_id>/", views.CommentLikeAPIView.as_view(), name="comment_like"),
]
