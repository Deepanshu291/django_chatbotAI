from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register(r'chatsessions', ChatSessionViewSet, basename='chatsession')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('chatsessions/', ChatSessionListCreateAPIView.as_view(), name='chat-session-list-create'),
    path('chatsessions/<int:pk>/', ChatSessionDetailAPIView.as_view(), name='chat-session-detail'),

    # Messages (within a session)
    path('chatsessions/<int:session_pk>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),

    # path('chatsessions/<int:session_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='messages'),
    # path('', include(router.urls)),
]
