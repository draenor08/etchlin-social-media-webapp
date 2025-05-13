from django.urls import path
from . import views

urlpatterns = [
    path('auth/check/', views.check_auth, name='check_auth'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<str:user_id>/', views.get_profile, name='get_profile'),
    path('profile/upload/picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('auth/user/', views.get_user_info, name='get_user_info'),
    path('profile/update/bio/', views.update_bio, name='update_bio'),
    path('search/', views.search_users, name='search_users'),
]