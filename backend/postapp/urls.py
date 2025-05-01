from django.urls import path
from .views import create_post, user_feed

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('feed/', user_feed, name='user_feed'),
]
