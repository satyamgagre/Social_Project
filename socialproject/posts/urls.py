from django.urls import path
from . import views

urlpatterns = [
    path('create',views.post_create, name="create"),
    path('feed',views.feed, name="feed"),
    path('like/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
]