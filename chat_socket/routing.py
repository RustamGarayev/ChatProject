from django.urls import re_path

from chat_socket import consumers

app_name = 'chat_socket'

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi(), name="chat-room-consumer"),
]
