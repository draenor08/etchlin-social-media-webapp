from django.urls import path
from . import views

urlpatterns = [
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/<str:user_id>/', views.get_user_profile, name='get_user_profile'),
]
