from django.urls import path
from . import views  # this imports from userapp/views.py

urlpatterns = [
    path('<str:user_id>/send_request/', views.follow_user, name='send_request'),
    path('<str:user_id>/respond/', views.respond_request, name='respond'),
    path('friends/', views.get_friends, name='get_friends'),
]