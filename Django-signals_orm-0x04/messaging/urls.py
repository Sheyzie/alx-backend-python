from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet, UserViewset

# Top-level router for conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'users', UserViewset, basename='users')

# Nested router for messages inside conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
