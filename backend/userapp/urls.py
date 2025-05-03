from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_id>/profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('<str:user_id>/profile/', views.get_user_profile, name='get_user_profile'),
]
