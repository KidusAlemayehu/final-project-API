from django.urls import path, include
from .views import MessageSendAPIView, MessageListView

urlpatterns = [
    path('msg/send/', MessageSendAPIView.as_view(), name="send_message"),
    path('msg/list/', MessageListView.as_view(), name="message_list"),
]
