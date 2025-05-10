from django.urls import path
from .views import create_comment

urlpatterns = [
    path('comment/create/', create_comment, name='create_comment'),
]
