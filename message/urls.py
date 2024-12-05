from django.urls import path
from .views import send_message, messages, conversation_list

app_name = 'message'

urlpatterns = [
    path('send/<int:receiver_id>/', send_message, name='send_message'),
    path('<int:receiver_id>/', messages, name='message'),
    path('conversations/', conversation_list, name='conversation_list'),
]
