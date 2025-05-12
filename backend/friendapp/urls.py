from django.urls import path
from . import views  # this imports from userapp/views.py

urlpatterns = [
    path('send_request/', views.send_request, name='send_request'),
    path('respond/', views.respond_request, name='respond'),
    path('friends/', views.get_friends, name='get_friends'),
    path('friend/remove/', views.remove_friend, name='remove_friend'),
    path('friends/count/<str:user_id>/', views.friend_count, name='friend_count'),
    path('friends/status/<str:user_id>/', views.friend_status, name='friend_status'),
    path('friends/requests/', views.get_requests, name='get_requests'),
]