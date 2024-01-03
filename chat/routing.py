# chat/routing.py

from django.urls import re_path
from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[\w\s]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/priv/$', ChatConsumer.as_asgi()),
]


