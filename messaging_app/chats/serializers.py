from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Message, Conversation


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['id', 'role','created_at']
        
    def create(self, validated_data):
        password = validated_data.pop('password_hash')
        role = self.context.get('role')

        if not role:
            validated_data['role'] = 'guest'
        if not password:
            raise ValidationError("Password is required.")
        
        user = User(**validated_data)
        user.set_password(password)  # hashes the password properly
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password_hash', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.SerializerMethodField()
    recipient_id = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Message.objects.all(),
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'recipient_id', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender_id', 'sent_at']

    def get_sender_id(self, obj):
        sender_id = self.context.get('request').user.id
        if not sender_id:
            raise serializers.ValidationError('No sender ID found')
        return sender_id

    def create(self, validated_data):
        sender_id = self.context.get('sender_id')
        sender = get_object_or_404(User, id=sender_id)

        # remove if exist
        validated_data.pop('sender_id', None)

        message = Message(sender_id=sender, **validated_data)
        message.save()
        return message 
    

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # nested representation
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source='participants'  # points to the `participants` field
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation