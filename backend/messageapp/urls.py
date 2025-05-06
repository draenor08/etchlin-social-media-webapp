from django.urls import path
from . import views 

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('<int:other_user_id>/messages/', views.get_conversation, name='get_conversation'),
]
