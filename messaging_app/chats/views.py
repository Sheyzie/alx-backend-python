from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Add current user to participants automatically (if not already added by serializer)
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        conversation = self.get_object()

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant in this conversation."}, status=403)

        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='messages')
    def send_message(self, request, pk=None):
        conversation = self.get_object()

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant in this conversation."}, status=403)

        data = request.data.copy()
        data['conversation'] = str(conversation.conversation_id)

        serializer = MessageSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        message = serializer.save(sender=request.user)
        return Response(MessageSerializer(message).data, status=201)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=201, headers=headers)
