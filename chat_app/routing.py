from django.urls import path, include
from .consumers import ChatConsumer
from django.urls import re_path


# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<userId>\w+)/$', ChatConsumer.as_asgi()),

]
