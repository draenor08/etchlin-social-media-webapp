from django.urls import path
from . import views 

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('messages/<int:other_user_id>/', views.get_conversation, name='get_conversation'),
]
