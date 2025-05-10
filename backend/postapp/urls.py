from django.urls import path
from . import views

urlpatterns = [
    path('post/create/', views.create_post, name='create_post'),
    path('post/feed/', views.user_feed, name='user_feed'),
    path('post/edit/', views.update_post, name='post_edit'),
    path('post/delete/', views.delete_post, name='post_delete'),
]
