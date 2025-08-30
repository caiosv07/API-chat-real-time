from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<str:sala_name>", consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    #url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    path("ws/test/", consumers.TestConsumer.as_asgi()),

]