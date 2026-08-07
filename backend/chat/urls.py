from django.urls import path

from .views import (
    MyConversationAPIView,
    AdminConversationListAPIView,
    ConversationCreateAPIView,
    ConversationMessagesAPIView,
)


urlpatterns = [

    path(
        "my/",
        MyConversationAPIView.as_view(),
        name="my-conversation",
    ),

    path(
        "admin/",
        AdminConversationListAPIView.as_view(),
        name="admin-conversations",
    ),

    path(
        "create/",
        ConversationCreateAPIView.as_view(),
        name="create-conversation",
    ),

    path(
        "<int:conversation_id>/messages/",
        ConversationMessagesAPIView.as_view(),
        name="conversation-messages",
    ),

]