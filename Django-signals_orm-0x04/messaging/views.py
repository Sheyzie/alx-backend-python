from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView


from .auth import CustomTokenObtainPairSerializer
from .permissions import IsParticipantOfConversation, IsMessageOwner
from .models import Conversation, Message, MessageHistory
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer, MessageHistorySerializer
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination
from .filters import MessageFilter


User = get_user_model()

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = LargeResultsSetPagination
    filter_backends = [MessageFilter]
    filterset_fields = ['participants']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')  # note the lookup key
        # will break since there is no field for conversation in message
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by('sent_at')

    def perform_create(self, serializer):
        # Add current user to participants automatically (if not already added by serializer)
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    # @action(detail=True, methods=['get'], url_path='messages')
    # def messages(self, request, pk=None):
    #     conversation = self.get_object()

    #     if request.user not in conversation.participants.all():
    #         return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

    #     messages = conversation.messages.all().order_by('sent_at')
    #     serializer = MessageSerializer(messages, many=True)
    #     return Response(serializer.data)

    # @action(detail=True, methods=['post'], url_path='messages')
    # def send_message(self, request, pk=None):
    #     conversation = self.get_object()

    #     if request.user not in conversation.participants.all():
    #         return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

    #     data = request.data.copy()
    #     data['conversation'] = str(conversation.conversation_id)

    #     serializer = MessageSerializer(data=data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     message = serializer.save(sender=request.user)
    #     return Response(MessageSerializer(message).data, status=201)
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageOwner]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        # Check if user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data, context={
            'request': request,
            'conversation': conversation
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MessageEditHistory(viewsets.ModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
