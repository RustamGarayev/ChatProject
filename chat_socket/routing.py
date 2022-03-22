from django.urls import re_path
from django.conf.urls import url

from chat_socket import consumers

app_name = 'chat_socket'

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi(), name="chat-room-consumer"),
    # re_path(r'ws/chat/(?P<slug>\w+)/$', consumers.ChatConsumer.as_asgi(), name="chat-room-consumer"),
]