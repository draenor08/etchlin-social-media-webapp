from django.urls import path
from .views import create_like

urlpatterns = [
    path('create/', create_like, name='create_like'),
]
