from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


ROLE_CHOICES = [
    ('guest', 'Guest'),
    ('host', 'Host'),
    ('admin', 'Admin'),
]

class User(AbstractUser):
    username = None # made this none to get pass integrity error
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=50, null=False, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password_hash', 'role']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey('user', on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey('user', on_delete=models.CASCADE, related_name='message_reciever')
    conversation = models.ForeignKey('conversation', on_delete=models.CASCADE, related_name='message')
    content = models.TextField()
    edited = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender}: {self.content}'


class MessageHistory(models.Model):
    message_history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey('message', on_delete=models.CASCADE)
    message_body = models.TextField()
    edited_by = models.ForeignKey('user', on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField('user', related_name='conversation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = self.participants.all()
        if users.count() == 2:
            return f"Chat: {users[0].first_name} - {users[1].first_name}"
        return f"Conversation ({self.conversation_id})" 


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.ForeignKey('user', on_delete=models.CASCADE)
    message = models.ForeignKey('message', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)