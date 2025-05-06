from django.urls import path
from . import views 

urlpatterns = [
    path('<str:user_id>/send_message/', views.send_message, name='send_message'),
    path('<str:user_id>/messages/', views.get_conversation, name='get_conversation'),
] 