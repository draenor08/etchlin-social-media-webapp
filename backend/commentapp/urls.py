from django.urls import path
from .views import create_comment

urlpatterns = [
    path('comment/', create_comment, name='create_comment'),
]
