from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Message, Conversation, MessageHistory


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'password_hash', 'role', 'created_at']
        read_only_fields = ['user_id', 'role','created_at']
        
    def create(self, validated_data):
        password_hash = validated_data.pop('password_hash')
        role = self.context.get('role')

        if not role:
            validated_data['role'] = 'guest'
        if not password_hash:
            raise ValidationError("Password is required.")
        
        user = User(**validated_data)
        user.set_password(password_hash)  # hashes the password properly
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
    # sender = serializers.SerializerMethodField()
    receiver = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'receiver', 'conversation', 'content', 'timestamp']
        read_only_fields = ['message_id', 'sender', 'conversation', 'timestamp']

    # def get_message_id(self, obj):
    #     return obj.sender

    def create(self, validated_data):
        sender = self.context['request'].user
        conversation = self.context['conversation']
        validated_data['sender'] = sender
        validated_data['conversation'] = conversation
        return super().create(validated_data)

    

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
    

class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['message_history_id', 'message', 'message_body', 'edited_at', 'edited_by']
        read_only_fields = ['message_history_id', 'message', 'message_body', 'edited_at', 'edited_by']
