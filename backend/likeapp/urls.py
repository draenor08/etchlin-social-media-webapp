from django.urls import path
from .views import like_post

urlpatterns = [
    path('like/', like_post, name='create_like'),
]
